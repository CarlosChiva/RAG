// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CollectionsService } from '../../services/collections.service';
import { UploadComponent } from '../../components/upload_pdf/upload_pdf.component'; // Importar componente
import {DomSanitizer, SafeHtml} from '@angular/platform-browser';
import {marked } from 'marked';
import {ChatOutputComponent} from '../../components/chat-output/chat-output.component';
import {SidebarComponent} from '../../components/sidebar/sidebar.component';
import {SidebarItemComponent} from '../../components/sidebar-pdf-item/sidebar-pdf-item.component';
import {ButtonContainerComponent} from '../../components/button-container/button-container.component';
import {UserInputComponent} from '../../components/user-input/user-input.component';

interface UserMessage {
  user: string;
}

interface BotMessage {
  bot: string;
}
type ConversationMessage = UserMessage | BotMessage;

@Component({
  selector: 'app-pdf',
  standalone: true,
  imports: [CommonModule, HttpClientModule,  FormsModule,UploadComponent,ChatOutputComponent,SidebarComponent,SidebarItemComponent,ButtonContainerComponent,UserInputComponent],
  templateUrl: './rag_pdf.component.html',
  styleUrls: ['./rag_pdf.component.scss']
})
// Define interfaces para tus tipos de mensajes

// Tipo unión para cualquier tipo de mensaje

export class PdfComponent implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;
  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarItemComponent) sidebarItemComponent!: SidebarItemComponent;

  
  sidebarCollapsed = false;
  collections: string[] = [];
  conversation: any[] = [];

  selectedCollection: string | null = null;
  message: string = '';
  currentMessage: string = '';

  //messages: Message[] = [];
  isSending: boolean = false;
  mostrarModal: boolean = false;
  // Añade esta interfaz y la propiedad messages
  messages: {
    text: string|Promise<String>|SafeHtml;
    isUser: boolean;
    isTyping?: boolean;
  }[] = [];


  constructor(
    private collectionsService: CollectionsService,
    private sanitizer:DomSanitizer,

  ) { }
  abrirModal() {
    this.mostrarModal = true;
    document.body.classList.add('modal-open'); // Bloquea el fondo
  }

  cerrarModal() {
    this.mostrarModal = false;
    document.body.classList.remove('modal-open');
    this.ngOnInit();
}
  ngOnInit(): void {
    this.loadCollections();
  }
  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
    this.sidebarComponent.toggleSidebar();
  }


  loadCollections(): void {
    this.collectionsService.getCollections().subscribe({
      next: (data: {collections_name: string[]}) => {
        this.collections = data.collections_name;
        
        if (this.collections.length === 0) {
          this.abrirModal();
        }
      },
      error: (error: any) => console.error('Error fetching collections:', error)
    });
  }

  renderConversation(conversation: any[]): void {
    this.messages=[]
    conversation.forEach((message) => {
      if ('user' in message) {
        this.messages.push({ text: message.user, isUser: true });
      } else if ('bot' in message) {
        this.messages.push({ text: this.markdownRender(marked(message.bot)), isUser: false });
      }
    });
  
    this.scrollChatToBottom();
  }
  selectCollection(collection:string){
    this.selectedCollection=collection;
  }
  deleteCollection(collectionName: string): void {
   // event.stopPropagation(); // Prevent triggering selectCollection
    this.loadCollections();
  }


  onMessageChange(message: string): void {
    this.currentMessage = message;
  }
  sendMessage(messageFromChild?: string): void {
    // Usar el mensaje del hijo si viene, sino usar this.message (compatibilidad)
    const messageText = messageFromChild || this.message || this.currentMessage;
    const trimmedMessage = messageText.trim();

    if (!messageText || !this.selectedCollection) {
      alert('Please enter a message and select a collection.');
      return;
    }
    
    this.isSending = true;
    
    // Añadir mensaje del usuario
    this.messages.push({
      text: messageText,
      isUser: true
    });
    
   this.message = '';
    this.currentMessage = '';
    
    this.scrollChatToBottom();
    
    // Añadir mensaje del bot con estado "typing"
    const botMessageIndex = this.messages.length;
    this.messages.push({
      text: '',
      isUser: false,
      isTyping: true
    });
    
    this.collectionsService.sendMessage(trimmedMessage, this.selectedCollection).subscribe({
      next: (data: string) => {

        // Iniciar animación de escritura
        this.typeTextInMessage(botMessageIndex, data);
      },
      error: (error: any) => {
        console.error('Error sending message:', error);
        // Actualizar mensaje con error
        this.messages[botMessageIndex] = {
          text: 'Error: Could not get response',
          isUser: false
        };

      },
      complete: () => {
      }
    });
  }
  markdownRender(message:string | Promise<String>){
    return this.sanitizer.bypassSecurityTrustHtml(message as string);
       
  }
typeTextInMessage(messageIndex: number, fullText: string, speed: number = 20): void {
  let index = 0;
  const message = this.messages[messageIndex];
  
  const addNextChar = () => {
    if (index < fullText.length) {
      // Actualizar el texto letra por letra
      const markdownText=marked(fullText.substring(0, index + 1))
      const messageRenderized= this.markdownRender(markdownText)
      this.messages[messageIndex] = {
        ...message,
        text: messageRenderized,
        isTyping: true
      };
      
      index++;
      setTimeout(addNextChar, speed);
      
      // // Hacer scroll hacia abajo mientras se escribe
      // if (this.chatOutputComponent) {
      //   this.chatOutputComponent.scrollToBottom();
      // }
    } else {
      const markdownText = marked(fullText);
      const safeHtml = this.sanitizer.bypassSecurityTrustHtml(markdownText as string);
      
      // Finalizar la animación
      this.messages[messageIndex] = {
        ...message,
        text: safeHtml,
        isTyping: false
      };
            this.isSending = false;

    }
  };
  
  addNextChar();
}
  
  handleKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.sendMessage();
    }
  }
  private scrollChatToBottom(): void {
    setTimeout(() => {
     if (this.chatOutputComponent) {
        this.chatOutputComponent.scrollToBottom();
      }
    });
  }
};

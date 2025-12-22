import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatOutputComponent } from '../../components/chat-output/chat-output.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ExcelService } from '../../services/excel.service';
import { Router, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import {marked } from 'marked';

import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarExcelItemComponent } from '../../components/sidebar-excel-item/sidebar-excel-item.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';
import { ExcelUploaderComponent } from '../../components/excel-uploader/excel-uploader.component';
interface UserMessage {
  user: string;
}

interface BotMessage {
  bot: string;
}
type ConversationMessage = UserMessage | BotMessage;

@Component({
  selector: 'app-excels',
  imports: [
    HttpClientModule,
    CommonModule,
    SidebarComponent,
    
    SidebarExcelItemComponent,
    ChatOutputComponent,
    ButtonContainerComponent,
    UserInputComponent,
    ExcelUploaderComponent
  ],
  templateUrl: './excels.component.html',
  styleUrl: './excels.component.scss'
})
export class Excels implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;
  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarExcelItemComponent) sidebarItem!: SidebarExcelItemComponent;
  conversation: any[] = [];

  // Properties from template
  collections: any[] = [];
  selectedCollection: any = null;
  // messages: any[] = [];
  isSending: boolean = false;
  currentMessage: string = '';
  message: string = '';
  sidebarCollapsed: boolean = false;
  mostrarModal: boolean = false;
  files: string[] = [];
  messages: {
    text: string|Promise<String>|SafeHtml;
    isUser: boolean;
    isTyping?: boolean;
  }[] = [];

  constructor(
    private configsService: ExcelService,
    private router: Router,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.loadConfigs();
  }

  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  loadConfigs(): void {
    this.configsService.listFiles().subscribe({
      next: (response: any) => {
        this.files = response.files;
        console.log(this.files)
        // Open modal if no files are available
        if (this.files.length === 0) {
          this.abrirModal();
        }
      },
      error: (error: any) => console.error('Error fetching collections:', error)
    });
  }

  selectCollection(collection: any): void {
    this.selectedCollection = collection;
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

  deleteCollection(collection: any): void {
    // Remove the collection from the files array
    this.files = this.files.filter(file => file !== collection);
    // Optionally, if the deleted collection was selected, deselect it
    if (this.selectedCollection === collection) {
      this.selectedCollection = null;
    }
    // Check if we need to open the modal when there are no files left
    if (this.files.length === 0) {
      this.abrirModal();
    }
  }

  toggleShowFile(file: string): void {
    // Handle file show/hide toggle
    console.log('Toggle show for file:', file);
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
    
    // Variable para acumular el mensaje completo
    let accumulatedText = '';
    
    this.configsService.sendMessage(trimmedMessage, this.selectedCollection).subscribe({
    next: (data: string) => {
      console.log(data)
        // Si recibimos un mensaje especial de finalización, terminamos
        if (data === '__END__') {
          // Finalizar el mensaje actual
          const markdownText = marked(accumulatedText);
          const safeHtml = this.markdownRender(markdownText);
          
          this.messages[botMessageIndex] = {
            text: safeHtml,
            isUser: false,
            isTyping: false
          };
          this.isSending = false;
          return;
        }
        // Acumular el texto recibido
        accumulatedText += data;
        
        // Actualizar el mensaje con el texto acumulado (sin animación)
        const markdownText = marked(accumulatedText);
        const safeHtml = this.markdownRender(markdownText);
        
        this.messages[botMessageIndex] = {
          text: safeHtml,
          isUser: false,
          isTyping: true
        };
      },
      error: (error: any) => {
        console.error('Error sending message:', error);
        // Actualizar mensaje con error
        this.messages[botMessageIndex] = {
          text: 'Error: Could not get response',
          isUser: false
        };
        this.isSending = false;
      },
      complete: () => {
        // Finalizar el mensaje cuando se complete la conexión
        if (accumulatedText) {
          const markdownText = marked(accumulatedText);
          const safeHtml = this.markdownRender(markdownText);
          
          this.messages[botMessageIndex] = {
            text: safeHtml,
            isUser: false,
            isTyping: false
          };
        } else {
          this.messages[botMessageIndex] = {
            text: 'No response received',
            isUser: false,
            isTyping: false
          };
        }
        this.isSending = false;
      }
    });
  }

  markdownRender(message: string | Promise<String>) {
    return this.sanitizer.bypassSecurityTrustHtml(message as string);
  }

  abrirModal(): void {
    this.mostrarModal = true;
  }

  cerrarModal(): void {
    this.mostrarModal = false;
    // Reload files after closing the modal (to show newly uploaded files)
    this.loadConfigs();
  }

  onFileUploaded(): void {
    // This method is called when a file is successfully uploaded
    // Reload the file list to show the new file
    this.loadConfigs();
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
}

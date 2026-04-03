import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatOutputChatbotComponent } from '../../components/chat-output-chatbot/chat-output-chatbot.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ExcelService } from '../../services/excel.service';
import { Router, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import {marked } from 'marked';
import { ChatMessage } from '../../interfaces/chat-message';

import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarExcelItemComponent } from '../../components/sidebar-excel-item/sidebar-excel-item.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';
import { ExcelUploaderComponent } from '../../components/excel-uploader/excel-uploader.component';

@Component({
  selector: 'app-excels',
  imports: [
    HttpClientModule,
    CommonModule,
    SidebarComponent,
    
    SidebarExcelItemComponent,
    ChatOutputChatbotComponent,
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
  @ViewChild(ChatOutputChatbotComponent) chatOutputComponent!: ChatOutputChatbotComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarExcelItemComponent) sidebarItem!: SidebarExcelItemComponent;
  conversation: any[] = [];
  private currentBotMessageIndex: number | null = null;
  rawResponse:string="";
  messages: ChatMessage[] = [];

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
    this.messages = conversation.map((msg) => {
      if ('user' in msg) {
        return {
          text: msg.user,
          isUser: true,
          isTyping: false,
          eventHeader: '',
          thinkingTokens: [],
          responseText: '',
          showThinking: false,
        } as ChatMessage;
      }
      if ('bot' in msg) {
        const botText: string = msg.bot as string;
        const thinkingTokens: string[] = [];
        const remainingText = botText.replace(/<think>(.*?)<\/think>/gs, (match, p1) => {
          thinkingTokens.push(p1);
          return '';
        }).trim();
        let renderedContent: SafeHtml;
        renderedContent = this.markdownRender(remainingText);
        return {
          text: '',
          isUser: false,
          isTyping: false,
          eventHeader: 'AI Response',
          thinkingTokens: thinkingTokens,
          responseText: renderedContent,
          showThinking: true,
        } as ChatMessage;
      }
      return {
        text: '',
        isUser: false,
        isTyping: false,
        eventHeader: '',
        thinkingTokens: [],
        responseText: '',
        showThinking: false,
      } as ChatMessage;
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
    this.currentBotMessageIndex = botMessageIndex;
    
    this.configsService.sendMessage(trimmedMessage, this.selectedCollection).subscribe({
    next: (data) => this.handleIncoming(data),
      
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
        if (this.currentBotMessageIndex !== null) {
          this.messages[this.currentBotMessageIndex].isTyping = false;
        }
        this.isSending = false;
        this.currentBotMessageIndex = null;
        this.rawResponse = '';
      }
    });
  }
  handleIncoming(data: any): void {
    if (this.currentBotMessageIndex === null) return;

    const currentMessage = this.messages[this.currentBotMessageIndex];

    try {
      if (data.event) {
        switch (data.event) {
          case 'response':
            this.handleResponseEvent(data, currentMessage);
            break;
          default:
            // Otros eventos como "Routing..." - SIEMPRE actualizar el header
            currentMessage.eventHeader = data.event;
            break;
        }
      } else {
        // Si no tiene event, podría ser un mensaje directo de texto
        this.appendToResponse(data, currentMessage);
      }
    } catch (error) {
      console.error('Error processing WebSocket message:', error, data);
    }
  }

  markdownRender(message: string | Promise<String>) {
    return this.sanitizer.bypassSecurityTrustHtml(message as string);
  }
  handleResponseEvent(data: any, currentMessage: ChatMessage): void {
    if (data.step === 'thinking') {
      // SIEMPRE actualizar header cuando está pensando
      currentMessage.eventHeader = 'AI Thinking';
      
      // Añadir token al thinking
      if (data.token) {
        if (!currentMessage.thinkingTokens) {
          currentMessage.thinkingTokens = [];
        }
        currentMessage.thinkingTokens.push(data.token);
      }
    } else if (data.step === 'response') {
      // SIEMPRE actualizar header cuando está respondiendo
      currentMessage.eventHeader = 'AI Response';
      
      // Añadir texto de respuesta
      if (data.response) {
        if (!currentMessage.responseText) {
          currentMessage.responseText = '';
        }
         this.rawResponse+= data.response
        currentMessage.responseText =this.sanitizer.bypassSecurityTrustHtml(marked(this.rawResponse)as string); 
        
      }
    }
  }

  appendToResponse(data: any, currentMessage: ChatMessage): void {
    // Manejar mensajes que no tienen estructura de evento específica
    if (typeof data === 'string') {
      if (!currentMessage.responseText) {
        currentMessage.responseText = '';
      }
      currentMessage.responseText += data;
      
      if (typeof currentMessage.responseText === 'string') {
        const markdownText = marked(currentMessage.responseText);
        currentMessage.responseText = this.sanitizer.bypassSecurityTrustHtml(markdownText as string);
      }
    }
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

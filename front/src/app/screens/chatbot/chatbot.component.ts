// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { marked } from 'marked';
import { UploadComfyComponent } from '../../components/upload_comfy_conf/upload_comfy.component';
import { ChatOutputChatbotComponent } from '../../components/chat-output-chatbot/chat-output-chatbot.component';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarItemComponent } from '../../components/sidebar-conversations-item/sidebar-conversations-item.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ModelsListComponent } from '../../components/models-list/models-list.component';
import { UserInputChatbotComponent } from '../../components/user-input-chatbot/user-input-chatbot.component';

import { Config } from '../../interfaces/config.interface';
import { ModelItem } from '../../interfaces/models.inferface';
import { ChatMessage } from '../../interfaces/chat-message';

import { ModelsService } from '../../services/models.service';



@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ChatOutputChatbotComponent,
    SidebarComponent,
    SidebarItemComponent,
    ButtonContainerComponent,
    ModelsListComponent,
    UserInputChatbotComponent,
    UploadComfyComponent
  ],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;

  @ViewChild(ChatOutputChatbotComponent) chatOutputComponent!: ChatOutputChatbotComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarItemComponent) sidebarItemComponent!: SidebarItemComponent;
  @ViewChild(ModelsListComponent) modelsListComponent!: ModelsListComponent;

  private currentBotMessageIndex: number | null = null;
  messages: ChatMessage[] = [];

  selectedModel: ModelItem = { name: '', size: '' };  
  // Application state
  sidebarCollapsed = false;
  chats: string[] = [];
  chat: any[] = [];
  selectedChat: string | null = null;
  message: string = '';
  currentMessage: string = '';
  isSending: boolean = false;
  mostrarModal: boolean = false;
  rawResponse:string="";
  mcp_comfy_config:Object={};

  config: Config = {
    credentials: '',
    conversation: '',
    modelName: '',
    userInput: '',
    tools:{},
  };

  constructor(
    private ModelsService: ModelsService,
    private sanitizer: DomSanitizer,
  ) {}

  // Modal methods
  abrirModal() {
    this.mostrarModal = true;
    document.body.classList.add('modal-open');
  }


  ngOnInit(): void {
    this.loadChats();
  }
  
  cerrarModal() {
      this.mostrarModal = false;
      document.body.classList.remove('modal-open');
      this.ngOnInit();
  }

  // Sidebar methods
  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
    this.sidebarComponent.toggleSidebar();
  }

  onModelSelected(model: ModelItem): void {
    this.selectedModel = model as ModelItem;
  }

  loadChats(): void {
    this.ModelsService.getChats().subscribe({
      next: (data: { chats: string[] }) => {
        console.log("chat:", data);
        this.chats = data.chats.flatMap(item => Object.keys(item));
      },
      error: (error) => console.error('Error fetching collections:', error)
    });
  }

  // Conversation methods
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
  selectChat(chat: string) {
    this.selectedChat = chat;
  }

  deleteChat(collectionName: Event): void {
    this.loadChats();
  }

  onMessageChange(message: string): void {
    this.currentMessage = message;
  }
  sendMessage(messageFromChild?: string): void {
    const messageText = messageFromChild || this.message || this.currentMessage;

    if (!messageText.trim() || !this.selectedChat) return;

    this.isSending = true;

    // Add user message
    this.messages.push({
      text: messageText,
      isUser: true
    });

    this.message = '';
    this.currentMessage = '';

    this.scrollChatToBottom();

    // Inicializar mensaje del bot con todos los campos necesarios
    this.currentBotMessageIndex = this.messages.length;
    this.messages.push({
      text: '',
      isUser: false,
      isTyping: true,
      eventHeader: '',
      thinkingTokens: [],
      responseText: '',
      showThinking: false
    });
    
    this.config = {
      credentials: '',
      userInput: messageText,
      conversation: this.selectedChat,
      modelName: this.selectedModel.name,
      tools: this.mcp_comfy_config,
    };

    console.log(this.config);
    this.ModelsService.query(this.config).subscribe({
      next: (data) => this.handlChatbottMessage(data),
      error: (error) => {
        if (this.currentBotMessageIndex !== null) {
          this.messages[this.currentBotMessageIndex] = { 
            text: 'Error: Could not get response', 
            isUser: false,
            isTyping: false
          };
        }
        console.error('WebSocket error:', error);
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

  handlChatbottMessage(data: any): void {

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
        currentMessage.responseText += this.sanitizer.bypassSecurityTrustHtml(markdownText as string);
      }
    }
  }

  markdownRender(message: string | Promise<string>): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(message as string);
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

  createChat(event: Event): void {
  let nameChat = "New_chat";
  let counter = 1;
    console.log("this.collections:",this.chats)

  // Check if the default name exists and increment the counter until a unique name is found
  while (this.chats.includes(nameChat)) {
    console.log("this.collections:",this.chats)
    nameChat = `New_chat_${counter}`;
    counter++;
  }

    this.ModelsService.createChat(nameChat).subscribe({
      next: () => { },
      error: (error) => console.error('Error fetching collections:', error)
    });

    this.loadChats();
  }
  onToolConfigSelected(config: Object): void {
    console.log('Tool configuration selected by the child:', config);
    if(!config || Object.keys(config).length === 0){
      console.log("No se encontraron datos",config);
      this.mostrarModal = true;
    }else{
        this.mcp_comfy_config=config;
    }

  }
 
}
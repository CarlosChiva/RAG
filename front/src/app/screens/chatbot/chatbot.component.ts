// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { marked } from 'marked';
import { UploadComponent } from '../../components/upload_pdf/upload_pdf.component';
import { ChatOutputChatbotComponent } from '../../components/chat-output-chatbot/chat-output-chatbot.component';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarItemComponent } from '../../components/sidebar-conversations-item/sidebar-conversations-item.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ModelsListComponent } from '../../components/models-list/models-list.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';

import { Config } from '../../interfaces/config.interface';
import { ModelItem } from '../../interfaces/models.inferface';
import { ChatMessage } from '../../interfaces/chat-message';

import { ModelsService } from '../../services/models.service';



@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    ChatOutputChatbotComponent,
    SidebarComponent,
    SidebarItemComponent,
    ButtonContainerComponent,
    ModelsListComponent,
    UserInputComponent,
    UploadComponent
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
  collections: string[] = [];
  collection: any[] = [];
  selectedCollection: string | null = null;
  message: string = '';
  currentMessage: string = '';
  isSending: boolean = false;
  mostrarModal: boolean = false;


  config: Config = {
    credentials: '',
    conversation: '',
    modelName: '',
    userInput: '',
    image: false,
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

  cerrarModal() {
    this.mostrarModal = false;
    document.body.classList.remove('modal-open');
    this.ngOnInit();
  }

  ngOnInit(): void {
    this.loadCollections();
  }

  // Sidebar methods
  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
    this.sidebarComponent.toggleSidebar();
  }

  onModelSelected(model: ModelItem): void {
    this.selectedModel = model as ModelItem;
  }

  loadCollections(): void {
    this.ModelsService.getChats().subscribe({
      next: (data: { collections_name: string[] }) => {
        console.log("chat:", data);
        this.collections = data.collections_name.flatMap(item => Object.keys(item));
      },
      error: (error) => console.error('Error fetching collections:', error)
    });
  }

  // Conversation methods
  renderConversation(conversation: any[]): void {
  // Cada elemento de conversation viene con la forma:
  // { user: 'texto del usuario' }   o   { bot: 'texto del bot' }
  this.messages = conversation.map((msg) => {
    // Si el objeto tiene la propiedad `user` -> mensaje del usuario
    if ('user' in msg) {
      return {
        text: msg.user,           // Texto tal cual
        isUser: true,             // Usuario
        // Campos que usa la UI y que se inicializan en `sendMessage`
        isTyping: false,
        eventHeader: '',
        thinkingTokens: [],
        responseText: '',
        showThinking: false,
      } as ChatMessage;
    }
    if ('bot' in msg) {
      // Ahora sabemos con certeza que 'msg.bot' es directamente la cadena que necesitamos.
      // Tu línea original 'const botText = msg.bot as string;' es CORRECTA.
      const botText: string = msg.bot as string;

      const thinkingTokens: string[] = [];

      const remainingText = botText.replace(/<think>(.*?)<\/think>/gs, (match, p1) => {
        const text= p1.split(" ")
        thinkingTokens.push(text); 
        return ''; 
      }).trim();
      let renderedContent: SafeHtml;

      renderedContent = this.markdownRender(remainingText); // Esta es la opción más probable si ya ves HTML en la salida previa.

      // Para depuración, puedes imprimir los valores para verificar:
      console.log(`Original botText:`, botText);
      console.log(`Content after removing <think> tags:`, remainingText);
      console.log(`Rendered responseText for display:`, renderedContent);
      console.log(`Extracted thinking tokens:`, thinkingTokens);

      return {
        text: '',                 // Los mensajes del bot usan responseText
        isUser: false,
        isTyping: false,
        eventHeader: 'AI Response',
        thinkingTokens: thinkingTokens,   // tokens extraídos de las etiquetas <think>
        responseText: renderedContent,    // Texto sin <think> tags, listo para mostrar
        showThinking: true,
      } as ChatMessage;
    }

    // Si el objeto no encaja en ninguno de los dos casos (ej. error),
    // devolvemos un objeto vacío para no romper el array.
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
  selectCollection(collection: string) {
    this.selectedCollection = collection;
  }

  deleteCollection(collectionName: string): void {
    this.loadCollections();
  }

  onMessageChange(message: string): void {
    this.currentMessage = message;
  }

  sendMessage(messageFromChild?: string): void {
    const messageText = messageFromChild || this.message || this.currentMessage;

    if (!messageText.trim() || !this.selectedCollection) return;

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
      conversation: this.selectedCollection,
      modelName: this.selectedModel.name,
      image: false,
    };

    console.log(this.config);
    this.ModelsService.query(this.config).subscribe({
      next: (data) => this.handleWebSocketMessage(data),
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
      }
    });
  }

  handleWebSocketMessage(data: any): void {
    if (this.currentBotMessageIndex === null) return;

    const currentMessage = this.messages[this.currentBotMessageIndex];

    try {
      // Manejar diferentes tipos de eventos
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
        currentMessage.responseText += data.response;
        
       
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

  markdownRender(message: string | Promise<string>): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(message as string);
  }

  typeTextInMessage(messageIndex: number, fullText: string, speed: number = 20): void {
    let index = 0;
    const message = this.messages[messageIndex];

    const addNextChar = () => {
      if (index < fullText.length) {
        // Update text character by character
        const markdownText = marked(fullText.substring(0, index + 1));
        const renderedMessage = this.markdownRender(markdownText);

        this.messages[messageIndex] = { ...message, text: renderedMessage, isTyping: true };
        index++;
        setTimeout(addNextChar, speed);
      } else {
        // End typing animation
        const markdownText = marked(fullText);
        const safeHtml = this.sanitizer.bypassSecurityTrustHtml(markdownText as string);

        this.messages[messageIndex] = { ...message, text: safeHtml, isTyping: false };
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

  createChat(event: Event): void {
  let nameChat = "New_chat";
  let counter = 1;
    console.log("this.collections:",this.collections)

  // Check if the default name exists and increment the counter until a unique name is found
  while (this.collections.includes(nameChat)) {
    console.log("this.collections:",this.collections)
    nameChat = `New_chat_${counter}`;
    counter++;
  }

    this.ModelsService.createChat(nameChat).subscribe({
      next: () => { },
      error: (error) => console.error('Error fetching collections:', error)
    });

    this.loadCollections();
  }
 
}
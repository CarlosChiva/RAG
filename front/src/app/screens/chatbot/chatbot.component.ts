// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { marked } from 'marked';
import { UploadComponent } from '../../components/upload_pdf/upload_pdf.component';
import { ChatOutputComponent } from '../../components/chat-output/chat-output.component';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarItemComponent } from '../../components/sidebar-conversations-item/sidebar-conversations-item.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ModelsListComponent } from '../../components/models-list/models-list.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';

import { Config } from '../../interfaces/config.interface';
import { ModelItem } from '../../interfaces/models.inferface';

import { ModelsService } from '../../services/models.service';

// Interfaces for message types
interface UserMessage {
  user: string;
}
interface BotMessage {
  bot: string;
}

type ConversationMessage = UserMessage | BotMessage;

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    ChatOutputComponent,
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

  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarItemComponent) sidebarItemComponent!: SidebarItemComponent;
  @ViewChild(ModelsListComponent) modelsListComponent!: ModelsListComponent;

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

  // Messages
  messages: {
    text: string | Promise<string> | SafeHtml;
    isUser: boolean;
    isTyping?: boolean;
  }[] = [];

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
    this.messages = conversation.map((message) => ({
      text: ('user' in message) ? message.user : this.markdownRender(marked(message.bot)),
      isUser: 'user' in message,
    }));

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

    // Add bot typing indicator
    const botMessageIndex = this.messages.length;
    this.messages.push({ text: '', isUser: false, isTyping: true });
    
    this.config = {
      credentials: '',
      userInput: messageText,
      conversation: this.selectedCollection,
      modelName: this.selectedModel.name,
      image: false,
    };

    console.log(this.config);
    this.ModelsService.query(this.config).subscribe({
      next: (data) => this.typeTextInMessage(botMessageIndex, data),
      error: () => {
        this.messages[botMessageIndex] = { text: 'Error: Could not get response', isUser: false };
      },
      complete: () => {}
    });
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
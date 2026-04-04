import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { marked } from 'marked';
import { ChatOutputChatbotComponent } from '../../components/chat-output-chatbot/chat-output-chatbot.component';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarItemComponent } from '../../components/sidebar-conversations-item/sidebar-conversations-item.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { UserInputChatbotComponent } from '../../components/user-input-chatbot/user-input-chatbot.component';
import { VideoPlayerComponent } from '../../components/video-player/video-player.component';

import { ChatMessage } from '../../interfaces/chat-message';

import { MultimediaService } from '../../services/multimedia.service';


@Component({
  selector: 'app-multimedia',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ChatOutputChatbotComponent,
    SidebarComponent,
    SidebarItemComponent,
    ButtonContainerComponent,
    UserInputChatbotComponent,
    VideoPlayerComponent
  ],
  templateUrl: './multimedia.screen.html',
  styleUrls: ['./multimedia.screen.scss']
})
export class MultimediaScreen implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;

  @ViewChild(ChatOutputChatbotComponent) chatOutputComponent!: ChatOutputChatbotComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(VideoPlayerComponent) videoPlayerComponent!: VideoPlayerComponent;

  private currentBotMessageIndex: number | null = null;
  messages: ChatMessage[] = [];

  // Application state
  conversations: any[] = [];
  currentConversation: any = null;
  selectedVideo: File | null = null;
  videoUrl: string | null = null;
  sidebarCollapsed = false;
  chat: any[] = [];
  selectedChat: string | null = null;
  message: string = '';
  currentMessage: string = '';
  isSending: boolean = false;
  rawResponse: string = '';

  constructor(
    private multimediaService: MultimediaService,
    private sanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.loadConversations();
  }

  // Sidebar methods
  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
    if (this.sidebarComponent) {
      this.sidebarComponent.toggleSidebar();
    }
  }

  // Conversation methods
  loadConversations(): void {
    this.multimediaService.listConversations().subscribe({
      next: (data: any) => {
        console.log('Conversations:', data);
        this.conversations = data.conversations || [];
      },
      error: (error) => console.error('Error fetching conversations:', error)
    });
  }

  loadConversation(conversationId: string): void {
    this.multimediaService.getConversation(conversationId).subscribe({
      next: (conversation: any) => {
        this.currentConversation = conversation;
        this.selectedChat = conversationId;
        this.renderConversation(conversation);
      },
      error: (error) => console.error('Error loading conversation:', error)
    });
  }

  renderConversation(conversation: any): void {
    this.currentConversation = conversation;
    const messages = conversation.messages || [];
    
    this.messages = messages.map((msg: any) => {
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

  selectChat(chat: string): void {
    this.selectedChat = chat;
  }

  deleteChat(conversationId: string): void {
    this.multimediaService.deleteConversation(conversationId).subscribe({
      next: () => {
        if (this.currentConversation?.id === conversationId) {
          this.currentConversation = null;
          this.selectedVideo = null;
          this.selectedChat = null;
        }
        this.loadConversations();
      },
      error: (error) => {
        console.error('Error deleting conversation:', error);
      }
    });
  }

  // Video methods
  handleVideoUpload(event: any): void {
    const file = event.target.files[0] as File;
    if (file) {
      this.selectedVideo = file;
      this.uploadVideo(file);
    }
  }

  uploadVideo(file: File): void {
    this.multimediaService.uploadVideo(file).subscribe({
      next: (response) => {
        console.log('Video uploaded:', response);
        // Set video URL after successful upload
        if (response.url) {
          this.videoUrl = response.url;
        } else {
          // Fallback to local file URL
          this.videoUrl = URL.createObjectURL(file);
        }
      },
      error: (error) => console.error('Error uploading video:', error)
    });
  }

  playVideo(): void {
    if (this.videoUrl && this.videoPlayerComponent) {
      this.videoPlayerComponent.play();
    }
  }

  onVideoEnded(): void {
    console.log('Video ended');
  }

  onPlaybackStateChanged(state: 'playing' | 'paused' | 'ended'): void {
    console.log('Playback state changed:', state);
  }

  // Message methods
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

    // Initialize bot message with all required fields
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
    
    this.multimediaService.sendMessage(this.selectedChat, messageText, (data) => {
      this.handleMultimediaMessage(data);
    }).subscribe({
      next: (data) => {},
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

  handleMultimediaMessage(data: any): void {
    if (this.currentBotMessageIndex === null) return;

    const currentMessage = this.messages[this.currentBotMessageIndex];

    try {
      if (data.event) {
        switch (data.event) {
          case 'response':
            this.handleResponseEvent(data, currentMessage);
            break;
          default:
            // Other events like "Routing..." - always update the header
            currentMessage.eventHeader = data.event;
            break;
        }
      } else {
        // If it doesn't have event, it could be a direct text message
        this.appendToResponse(data, currentMessage);
      }
    } catch (error) {
      console.error('Error processing WebSocket message:', error, data);
    }
  }

  handleResponseEvent(data: any, currentMessage: ChatMessage): void {
    if (data.step === 'thinking') {
      // Always update header when thinking
      currentMessage.eventHeader = 'AI Thinking';
      
      // Add token to thinking
      if (data.token) {
        if (!currentMessage.thinkingTokens) {
          currentMessage.thinkingTokens = [];
        }
        currentMessage.thinkingTokens.push(data.token);
      }
    } else if (data.step === 'response') {
      // Always update header when responding
      currentMessage.eventHeader = 'AI Response';
      
      // Add response text
      if (data.response) {
        if (!currentMessage.responseText) {
          currentMessage.responseText = '';
        }
        this.rawResponse += data.response;
        currentMessage.responseText = this.sanitizer.bypassSecurityTrustHtml(marked(this.rawResponse) as string);
      }
    }
  }

  appendToResponse(data: any, currentMessage: ChatMessage): void {
    // Handle messages that don't have specific event structure
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
    }, 100);
  }

  createChat(event?: Event): void {
    if (event) event.stopPropagation();
    let nameChat = `Chat ${Date.now()}`;

    // Check if the name exists and make it unique
    let counter = 1;
    while (this.conversations.some(c => c.id === nameChat || c.name === nameChat)) {
      nameChat = `Chat ${Date.now()}_${counter}`;
      counter++;
    }

    // Call backend to create conversation
    this.multimediaService.createConversation(nameChat).subscribe({
      next: (response) => {
        this.currentConversation = response;
        this.selectedChat = response.id;
        this.loadConversations();
      },
      error: (error) => {
        console.error('Error creating conversation:', error);
      }
    });
  }
}

import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatOutputChatbotComponent } from '../chat-output-chatbot/chat-output-chatbot.component';
import { ButtonContainerComponent } from '../button-container/button-container.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { SidebarItemComponent } from '../sidebar-conversations-item/sidebar-conversations-item.component';
import { ModelsListComponent } from '../models-list/models-list.component';
import { UserInputChatbotComponent } from '../user-input-chatbot/user-input-chatbot.component';
import { UploadMCPComponent } from '../upload_mcp_conf/upload_mcp.component';
import { UploadComfyComponent } from '../upload_comfy_conf/upload_comfy.component';
import { ChatMessage } from '../../interfaces/chat-message';

export class ChatbotInteractionBase implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild(ChatOutputChatbotComponent) chatOutputComponent!: ChatOutputChatbotComponent;
  
  // Application state
  sidebarCollapsed = false;
  chats: string[] = [];
  selectedChat: string | null = null;
  currentMessage: string = '';
  isSending: boolean = false;
  mostrarImageModal: boolean = false;
  mostrarMCPModal: boolean = false;
  currentEditConfig: any = {};
  mcp_comfy_config: Object = {};
  messages: ChatMessage[] = [];

  constructor() {}

  ngOnInit(): void {
    // Implementation in child components
  }
  
  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  // Methods to be implemented in child components
  onModelSelected(model: any): void {
    // Implementation in child components
  }

  loadChats(): void {
    // Implementation in child components
  }

  renderConversation(conversation: any[]): void {
    // Implementation in child components
  }

  selectChat(chat: string) {
    this.selectedChat = chat;
  }

  deleteChat(collectionName: Event): void {
    // Implementation in child components
  }

  onMessageChange(message: string): void {
    this.currentMessage = message;
  }

  openEditModal(tool: Object): void {
    if ('image_tools' in tool) {
      this.currentEditConfig = tool.image_tools;
      this.mostrarImageModal = true;
    }
    if ('mcp_tools' in tool) {
      this.currentEditConfig = tool.mcp_tools;
      this.mostrarMCPModal = true;
    }
  }

  // Modal methods
  cerrarImageModal(): void {
    this.mostrarImageModal = false;
  }

  cerrarMCPModal(): void {
    this.mostrarMCPModal = false;
  }

  private scrollChatToBottom(): void {
    setTimeout(() => {
      if (this.chatOutputComponent) {
        this.chatOutputComponent.scrollToBottom();
      }
    });
  }
}

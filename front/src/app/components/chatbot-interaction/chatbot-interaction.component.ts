import { Component } from '@angular/core';

@Component({
  selector: 'app-chatbot-interaction',
  template: `
    <div class="container">
      <app-models-list (modelSelected)="modelSelected.emit($event)" class="fixed-models-list"></app-models-list>
      <app-sidebar class="sidebar"
        [title]="'Chats'"
        [sidebarCollapsed]="sidebarCollapsed" 
        >
        <div sidebarContent>
          <button id="createChatButton"
            (click)="createChat.emit($event)" 
            class="add-button">
            +
          </button>
          <ul>
            <app-sidebar-conversations-item 
              *ngFor="let chat of chats"
              [collection]="chat"
              [isSelected]="selectedChat === chat"
              [displayField]="'chat'"
              (selectItem)="chatSelected.emit($event)"
              (conversationLoaded)="conversationLoaded.emit($event)"
              (itemDeleted)="itemDeleted.emit($event)">
            </app-sidebar-conversations-item>
          </ul>
          <app-button-container></app-button-container>
        </div>
      </app-sidebar>
      
      <button id="toggleSidebar" class="collapse-btn" (click)="toggleSidebar.emit()">☰</button> 

      <div class="main-content" [class.expanded]="sidebarCollapsed">
        <div class="chat-area" id="chat-area">
          <div class="chat-output">
            <app-chat-output-chatbot id="chat-output" [messages]="messages" ></app-chat-output-chatbot>
          </div>
          <app-user-input-chatbot
            class="user-input"
            [placeholder]="'Type your message here...'"
            [isSending]="isSending"
            [message]="currentMessage"
            [disabled]="!selectedChat"
            [sendButtonText]="'Send'"
            (messageChange)="messageChange.emit($event)"
            (sendMessage)="sendMessage.emit($event)"
            (toolConfigSelected)="toolConfigSelected.emit($event)"
            (editToolConfig)="editToolConfig.emit($event)">
          </app-user-input-chatbot> 

          <!-- Ventana Emergente -->
          <div class="overlay" *ngIf="mostrarImageModal">
            <div class="modal">
              <app-upload-Comfy
                [editConfig]="currentEditConfig"
                (cerrarImageModal)="cerrarImageModal.emit()"></app-upload-Comfy>
            </div>
          </div>
          <div class="overlay" *ngIf="mostrarMCPModal">
            <div class="modal">
              <app-upload-mcp 
                [editConfig]="currentEditConfig"
                (cerrarMCPModal)="cerrarMCPModal.emit()"></app-upload-mcp>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./chatbot-interaction.component.scss']
})
export class ChatbotInteractionComponent {
  // This component is just a structural template
  // All inputs and outputs are handled by parent components
}

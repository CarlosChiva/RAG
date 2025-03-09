// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CollectionsService } from '../../services/collections.service';
import { UploadComponent } from '../upload_pdf/upload_pdf.component'; // Importar componente

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
  imports: [CommonModule, HttpClientModule, RouterLink, FormsModule,UploadComponent],
  templateUrl: './rag_pdf.component.html',
  styleUrls: ['./rag_pdf.component.scss']
})
// Define interfaces para tus tipos de mensajes

// Tipo unión para cualquier tipo de mensaje

export class PdfComponent implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;

  
  sidebarCollapsed = false;
  collections: string[] = [];
  conversation: any[] = [];

  selectedCollection: string | null = null;
  message: string = '';
  
  //messages: Message[] = [];
  isSending: boolean = false;
  mostrarModal: boolean = false;
  // Añade esta interfaz y la propiedad messages
  messages: {
    text: string;
    isUser: boolean;
    isTyping?: boolean;
  }[] = [];


  constructor(
    private collectionsService: CollectionsService,
    private router: Router
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
  }

  logout(): void {
    if (confirm('Are you sure you want to logout?')) {
      localStorage.removeItem('access_token');
      this.router.navigate(['/login']);
    }
  }

  navigateToMenu(): void {
    this.router.navigate(['/menu']);
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

  selectCollection(collectionName: string): void {
    this.selectedCollection = collectionName;
    
    this.collectionsService.getConversation(collectionName).subscribe({
      next: (conversation: any) => {
        this.messages = [];
        console.log(conversation);
        
        conversation.forEach((message: any) => {
          if ('user' in message) {
            this.messages.push({
              text: message.user || '',
              isUser: true
            });
          }
          else if ('bot' in message) {
            this.messages.push({
              text: message.bot || '',
              isUser: false
            });
          }
        });
        
        this.scrollChatToBottom();
      },
      error: (error: any) => {
        console.error('Error loading conversation:', error);
      }
    });
  }

  deleteCollection(collectionName: string, event: Event): void {
    event.stopPropagation(); // Prevent triggering selectCollection
    this.collectionsService.deleteCollection(collectionName).subscribe({
      next: () => {
        this.collections = this.collections.filter(name => name !== collectionName);
      },
      error: (error: any) => console.error('Error deleting collection:', error)
    });
  }


  sendMessage(): void {
    const messageText = this.message.trim();
    
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
    
    // Limpiar el input
    this.message = '';
    
    this.scrollChatToBottom();
    
    // Añadir mensaje del bot con estado "typing"
    const botMessageIndex = this.messages.length;
    this.messages.push({
      text: '',
      isUser: false,
      isTyping: true
    });
    
    this.collectionsService.sendMessage(messageText, this.selectedCollection).subscribe({
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
        this.isSending = false;
      }
    });
  }

typeTextInMessage(messageIndex: number, fullText: string, speed: number = 20): void {
  let index = 0;
  const message = this.messages[messageIndex];
  
  const addNextChar = () => {
    if (index < fullText.length) {
      // Actualizar el texto letra por letra
      this.messages[messageIndex] = {
        ...message,
        text: fullText.substring(0, index + 1),
        isTyping: true
      };
      
      index++;
      setTimeout(addNextChar, speed);
      
      // Hacer scroll hacia abajo mientras se escribe
      if (this.chatOutput) {
        this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
      }
    } else {
      // Finalizar la animación
      this.messages[messageIndex] = {
        ...message,
        text: fullText,
        isTyping: false
      };
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
      if (this.chatOutput) {
        this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
      }
    });
  }
};

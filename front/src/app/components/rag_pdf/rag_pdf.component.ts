// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
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
  imports: [CommonModule, HttpClientModule, RouterLink, FormsModule],
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
  isSending = false;
  // Añade esta interfaz y la propiedad messages
  messages: {
    text: string;
    isUser: boolean;
    isTyping?: boolean;
  }[] = [];


  constructor(
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      alert('Token expired. Please, sign up again');
      this.router.navigate(['/login']);
      return;
    }
    
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
    const token = localStorage.getItem('access_token');
    
    this.http.get<{collections_name: string[]}>('http://127.0.0.1:8000/collections', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    }).subscribe({
      next: (data) => {
        this.collections = data.collections_name;
        
        if (this.collections.length === 0) {
          this.router.navigate(['/upload']);
        }
      },
      error: (error) => console.error('Error fetching collections:', error)
    });
  }

  selectCollection(collectionName: string): void {
    const token = localStorage.getItem('access_token');
    this.selectedCollection = collectionName;
    
  this.http.get<any>(`http://localhost:8000/get-conversation?collection_name=${collectionName}`, {
    headers: new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
  }).subscribe({
    next: (conversation) => {
      this.messages = [];
      console.log(conversation);
      
      conversation.forEach((message: ConversationMessage) => {
        if ('user' in message) {
          this.messages.push({
            text: message.user,
            isUser: true
          });
        }
        else if ('bot' in message) {
          this.messages.push({
            text: message.bot,
            isUser: false
          });
        }
      });
      
      setTimeout(() => {
        if (this.chatOutput) {
          this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
        }
      });
    },
    error: (error) => {
      console.error('Error loading conversation:', error);
    }
  });
  }

  deleteCollection(collectionName: string, event: Event): void {
    event.stopPropagation(); // Prevent triggering selectCollection
    const token = localStorage.getItem('access_token');
    
    if (this.selectedCollection === collectionName) {
      this.selectedCollection = null;
    }
    
    this.http.post('http://localhost:8000/delete-collection', 
      { collection_name: collectionName },
      {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        })
      }
    ).subscribe({
      next: () => {
        this.collections = this.collections.filter(name => name !== collectionName);
      },
      error: (error) => console.error('Error deleting collection:', error)
    });
  }

  sendMessage(): void {
    const messageText = this.message.trim(); // Declara la variable messageText
    
    if (!messageText || !this.selectedCollection) {
      alert('Please enter a message and select a collection.');
      return;
    }
    
    this.isSending = true;
    
    // Añadir mensaje del usuario
    this.messages.push({
      text: messageText, // Usa messageText aquí
      isUser: true
    });
    
    // Limpiar el input
    this.message = '';
    
    // Hacer scroll hacia abajo
    setTimeout(() => {
      if (this.chatOutput) {
        this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
      }
    });
    
    const token = localStorage.getItem('access_token');
    const params = new URLSearchParams({
      input: messageText, // Usa messageText aquí
      collection_name: this.selectedCollection
    });
    
    // Añadir mensaje del bot con estado "typing"
    const botMessageIndex = this.messages.length;
    this.messages.push({
      text: '',
      isUser: false,
      isTyping: true
    });
    
    this.http.get<string>(`http://localhost:8000/llm-response?${params.toString()}`, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      }),
      responseType: 'json' as any
    }).subscribe({
      next: (data) => {
        // Iniciar animación de escritura
        this.typeTextInMessage(botMessageIndex, data);
      },
      error: (error) => {
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
};

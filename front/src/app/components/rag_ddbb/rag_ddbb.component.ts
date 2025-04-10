// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DdbbServices } from '../../services/ddbb.service';
import  { DdbbConfComponent} from '../ddbb_conf/ddbb_conf.component';
import {DbConfig} from '../../interfaces/db-conf.interface';

interface UserMessage {
  user: string;
}

interface BotMessage {
  bot: string;
}
type ConversationMessage = UserMessage | BotMessage;

@Component({
  selector: 'app-rag-ddbb',
  standalone: true,
  imports: [CommonModule, HttpClientModule,  FormsModule,DdbbConfComponent],
  templateUrl: './rag_ddbb.component.html',
  styleUrls: ['./rag_ddbb.component.scss']
})

export class RagDdbbComponent {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;

  
  sidebarCollapsed = false;
  configs: DbConfig[] = [];
  conversation: any[] = [];
  dbConfig: DbConfig = {
    connection_name: '',
    type_db: '',
    user: '',
    password: '',
    host: '',
    port: '',
    database_name: '',
    database_path : ''
  };
  configList: DbConfig[] = [];
  selectedConfig: DbConfig = this.getEmptyConfig();


  message: string = '';
  
  isSending: boolean = false;
  mostrarModal: boolean = false;

  messages: {
    text: string;
    isUser: boolean;
    isTyping?: boolean;
  }[] = [];


  constructor(
    private configsService: DdbbServices,
    private router: Router,
  ) { }
  abrirModal(config?: DbConfig) {
    this.selectedConfig = config ? { ...config } : this.getEmptyConfig();
    this.mostrarModal = true;
    document.body.classList.add('modal-open');
  }
  private getEmptyConfig(): DbConfig {
    return { connection_name: '', type_db: '', user: '', password: '', host: '', port: '', database_name: '', database_path: '' };
  }
  cerrarModal() {
    this.mostrarModal = false;
    document.body.classList.remove('modal-open');
    this.ngOnInit();
}
  ngOnInit(): void {
    this.loadConfigs();
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

  loadConfigs(): void {
      this.configsService.getConfigs().subscribe({  
        next: (data:DbConfig[]) => {
          console.log(data);
  
          this.configList = data;
          console.log(this.configList);
        },
        error: (error) => console.error('Error fetching configurations:', error)      
      })
  
  
    }
  

    selectConfig(config: DbConfig): void {
      this.configsService.tryConnection(config).subscribe({
        next: (response: boolean) => {
        if (response) {
          this.selectedConfig = config; // Selecciona una configuración
        } else {
          console.log("Conexión fallida");
          alert("No se pudo conectar a la base de datos.");
    
        }
      },
      error: (error) => {
        const backendError = error?.error?.detail;
  
        console.error("Error de conexión:", error);
        alert(`❌ Error: ${backendError}`);
    
      },
     
    });
    };
    

    deleteConfig(config: DbConfig, event: Event): void {
      event.stopPropagation(); // Evita que se active `selectConfig`
      this.configsService.removeConfig(config).subscribe({
        next: () => {
          console.log('Configuration deleted:', config);
          alert('Configuration deleted successfully');
          this.loadConfigs(); // Recarga la lista de configuraciones
        },
        error: (error) => {
          console.error('Error deleting configuration:', error);
          alert('Error deleting configuration');
        }
      });
      this.configs = this.configs.filter(c => c !== config); // Elimina la configuración
    }


  sendMessage(): void {
    const messageText = this.message.trim();
    
    if (!messageText || !this.selectedConfig) {
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
    
    this.configsService.question(messageText, this.selectedConfig!).subscribe({
      next: (data: string) => {
        this.typeTextInMessage(botMessageIndex, data);
      },
      error: (error: any) => {
        console.error('Error sending message:', error);
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

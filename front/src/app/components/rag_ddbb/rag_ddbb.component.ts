// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DdbbServices } from '../../services/ddbb.service';
import  { DdbbConfComponent} from '../ddbb_conf/ddbb_conf.component';
import {DbConfig} from '../../interfaces/db-conf.interface';
import {ChatOutputComponent} from '../chat-output/chat-output.component';
import {SidebarComponent} from '../sidebar/sidebar.component';
import {SidebarItemComponent} from '../sidebar-ddbb-item/sidebar-ddbb-item.component';

import {DomSanitizer, SafeHtml} from '@angular/platform-browser';
import {marked } from 'marked';
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
  imports: [CommonModule, HttpClientModule,  FormsModule,DdbbConfComponent,ChatOutputComponent,SidebarComponent,SidebarItemComponent],
  templateUrl: './rag_ddbb.component.html',
  styleUrls: ['./rag_ddbb.component.scss']
})

export class RagDdbbComponent {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;
  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarItemComponent) sidebarItemComponent!: SidebarItemComponent;

  
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
  tableData: any[] = []; // Añade esta propiedad a la clase


  message: string = '';
  
  isSending: boolean = false;
  mostrarModal: boolean = false;

  messages: {
    text: string | Promise<String> | SafeHtml;
    isUser: boolean;
    isTyping?: boolean;
    tableData?: any;

  }[] = [];


  constructor(
    private configsService: DdbbServices,
    private router: Router,
    private sanitizer:DomSanitizer,
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
  

    onSelectItem(config: DbConfig): void {
      this.selectedConfig = config;
    }
    handleConnectionError(errorMessage: string): void {
      console.error('Connection error:', errorMessage);
      // Puedes implementar un manejo de errores adicional si es necesario
    }

    onItemDeleted(config: Event): void {
      // Actualizar la lista local después de la eliminación
    //  this.configList = this.configList.filter(c => c !== config);
      this.loadConfigs();
      // O, si prefieres recargar todos los datos
      // this.loadConfigs();
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
      next: (data: Object) => {
        var message=JSON.stringify(data);
        var dataParse = JSON.parse(message);
        const resultText = dataParse.result; // contendrá "Hay 2 personas en la lista."
        this.tableData = dataParse.table

            // Parse el string de la tabla a un objeto JavaScript
        if (typeof dataParse.table === 'string') {
          this.tableData = JSON.parse(dataParse.table);
        } else {
          this.tableData = dataParse.table;
        }
        
        console.log('Datos parseados:', this.tableData);
        
        
        this.typeTextInMessage(botMessageIndex, resultText); // 20 es la velocidad de escritura en milisegundos
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
      const markdownText=marked(fullText.substring(0, index + 1))
      const safeHtml=this.sanitizer.bypassSecurityTrustHtml(markdownText as string);
      this.messages[messageIndex] = {
        ...message,
        text: safeHtml,
        isTyping: true
      };
      
      index++;
      setTimeout(addNextChar, speed);
      
      // Hacer scroll hacia abajo mientras se escribe
      if (this.chatOutput) {
        this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
      }
    } else {
      const markdownText = marked(fullText);
      const safeHtml = this.sanitizer.bypassSecurityTrustHtml(markdownText as string);
      
      // Finalizar la animación
      this.messages[messageIndex] = {
        ...message,
        text: safeHtml,
        isTyping: false,
        tableData: this.tableData
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
      if (this.chatOutputComponent) {
        this.chatOutputComponent.scrollToBottom();
      }
    });
  }
};

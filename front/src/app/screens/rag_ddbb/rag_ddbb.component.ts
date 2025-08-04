// pdf.component.ts
import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { marked } from 'marked';

// Importar servicios
import { DdbbServices } from '../../services/ddbb.service';

// Importar interfaces
import { DbConfig } from '../../interfaces/db-conf.interface';

// Importar componentes individualmente
import { DdbbConfComponent } from '../../components/ddbb_conf/ddbb_conf.component';
import { ChatOutputComponent } from '../../components/chat-output/chat-output.component';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarItemComponent } from '../../components/sidebar-ddbb-item/sidebar-ddbb-item.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';

// Interfaces para tipos de mensajes
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
  imports: [
    CommonModule,
    HttpClientModule,
    FormsModule,
    DdbbConfComponent,
    ChatOutputComponent,
    SidebarComponent,
    SidebarItemComponent,
    ButtonContainerComponent,
    UserInputComponent
  ],
  templateUrl: './rag_ddbb.component.html',
  styleUrls: ['./rag_ddbb.component.scss']
})
export class RagDdbbComponent implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;

  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarItemComponent) sidebarItemComponent!: SidebarItemComponent;

  // Estado de la aplicación
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
    database_path: ''
  };

  configList: DbConfig[] = [];
  selectedConfig: DbConfig = this.getEmptyConfig();
  tableData: any[] = [];

  message: string = '';
  currentMessage: string = '';
  isSending: boolean = false;
  mostrarModal: boolean = false;

  messages: {
    text: string | Promise<string> | SafeHtml;
    isUser: boolean;
    isTyping?: boolean;
    tableData?: any[];
  }[] = [];

  constructor(
    private configsService: DdbbServices,
    private router: Router,
    private sanitizer: DomSanitizer
  ) {}

  // Modal methods
  abrirModal(config?: DbConfig) {
    this.selectedConfig = config ? { ...config } : this.getEmptyConfig();
    this.mostrarModal = true;
    document.body.classList.add('modal-open');
  }

  private getEmptyConfig(): DbConfig {
    return {
      connection_name: '',
      type_db: '',
      user: '',
      password: '',
      host: '',
      port: '',
      database_name: '',
      database_path: ''
    };
  }

  cerrarModal() {
    this.mostrarModal = false;
    document.body.classList.remove('modal-open');
    this.ngOnInit();
  }

  // Lifecycle hooks
  ngOnInit(): void {
    this.loadConfigs();
  }

  // Sidebar methods
  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  loadConfigs(): void {
    this.configsService.getConfigs().subscribe({
      next: (data: DbConfig[]) => {
        console.log(data);
        this.configList = data;
        console.log(this.configList);
      },
      error: (error) => console.error('Error fetching configurations:', error)
    });
  }

  onSelectItem(config: DbConfig): void {
    this.selectedConfig = config;
  }

  handleConnectionError(errorMessage: string): void {
    console.error('Connection error:', errorMessage);
  }

  // Actualizado para aceptar el evento
  onItemDeleted(deletedItem: DbConfig): void {
    
    // Actualizar la lista local después de la eliminación
//    this.loadConfigs();
    location.reload();
}

  onMessageChange(message: string): void {
    this.currentMessage = message;
  }

  sendMessage(messageFromChild?: string): void {
    const messageText = messageFromChild || this.message || this.currentMessage;

    if (!messageText.trim() || !this.selectedConfig) {
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
    this.currentMessage = '';

    this.scrollChatToBottom();

    // Añadir mensaje del bot con estado "typing"
    const botMessageIndex = this.messages.length;
    this.messages.push({ text: '', isUser: false, isTyping: true });

    this.configsService.question(messageText.trim(), this.selectedConfig!).subscribe({
      next: (event: any) => {
        if (event.response){
          console.log(event.response);
        }        
        if (event.table){
          console.log(event.table);
        }
        
      //   if (dataParse === 'end') {
      //     // Finalizar el mensaje actual
      //     return;
      //   }
    

      //   const resultText = dataParse.response;

      //   if (typeof dataParse.response === 'string') {
      //     console.log(dataParse.response);
      //     this.tableData = JSON.parse(dataParse.table);
      //   } else {
      //     this.tableData = dataParse.table;
      //   }

      //   console.log('Datos parseados:', this.tableData);

      //   this.typeTextInMessage(botMessageIndex, resultText); // 20 es la velocidad de escritura en milisegundos

    }
      ,
      error: (error: any) => {
        console.error('Error sending message:', error);
        this.messages[botMessageIndex] = { text: 'Error: Could not get response', isUser: false };
      }
    });
  }

  typeTextInMessage(messageIndex: number, fullText: string, speed: number = 20): void {
    let index = 0;
    const message = this.messages[messageIndex];

    const addNextChar = () => {
      if (index < fullText.length) {
        // Actualizar el texto letra por letra
        const markdownText = marked(fullText.substring(0, index + 1));
        const safeHtml = this.sanitizer.bypassSecurityTrustHtml(markdownText as string);
        this.messages[messageIndex] = { ...message, text: safeHtml, isTyping: true };

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
        this.messages[messageIndex] = { ...message, text: safeHtml, isTyping: false, tableData: this.tableData };
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
}
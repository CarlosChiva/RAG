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
  hasValidConfig: boolean = false;
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
    if (config) {
      this.selectedConfig = { ...config };
      this.hasValidConfig = true;
    } else {
      this.selectedConfig = this.getEmptyConfig();
      this.hasValidConfig = false;
    }
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
     this.hasValidConfig = true; 
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
   // Verificar que hay mensaje
    if (!messageText.trim()) {
      alert('Please enter a message.');
      return;
    }

    // Verificar que hay configuración válida seleccionada
    if (!this.hasValidConfig) {
      alert('Please select a configuration first.');
      return;
    }



    this.isSending = true;

    /* 1. Agregar mensaje del usuario */
    this.messages.push({ text: messageText, isUser: true });

    /* 2. Limpiar el input y hacer scroll */
    this.message = '';
    this.currentMessage = '';
    this.scrollChatToBottom();

    /* 3. Añadir “bot message” con estado typing */
    const botIdx = this.messages.length;
    this.messages.push({ text: '', isUser: false, isTyping: true });

    let accumulatedText = '';

    /* 4. Suscribirse al servicio WebSocket */
    this.configsService.question(messageText.trim(), this.selectedConfig!).subscribe({
      next: (event: any) => {
        // event puede ser {response: …}, {table: …} o {end: …}
        console.log('Response from API:', event);

        /* ---- 4.1. Respuesta de texto ---- */
        if (event.response) {
          accumulatedText += event.response;
          const html = this.sanitizer.bypassSecurityTrustHtml(
            marked(accumulatedText) as string
          );
          this.messages[botIdx] = {
            ...this.messages[botIdx],
            text: html,
            isTyping: true
          };
          setTimeout(() => this.scrollChatToBottom(), 0);
          return;
        }

        /* ---- 4.2. Tabla (JSON) ---- */
        if (event.table) {
          try {
            this.tableData = typeof event.table === 'string'
              ? JSON.parse(event.table)
              : event.table;
          } catch (_) {
            this.tableData = []; // fallback en caso de parsear mal
          }

          const html = this.sanitizer.bypassSecurityTrustHtml(
            marked(accumulatedText) as string
          );
          this.messages[botIdx] = {
            ...this.messages[botIdx],
            text: html,
            isTyping: false,
            tableData: this.tableData
          };
          return;
        }
        if (event.end){
          console.log('Received __END__ – closing socket');            
        }

        /* ---- 4.3. Error (JSON) ---- */
        if (event.error) {
          this.messages[botIdx] = {
            text: `Error: ${event.error}`,
            isUser: false
          };
          return;
        }
      },

      complete: () => {
        /* ---------- 5. Cierre automático ya está manejado por el servicio ----------
          Solo limpiamos el estado del UI. ------------------------------------- */
        this.isSending = false;
        console.log('WebSocket stream completed');
      },

      error: (err: any) => {
        console.error('Error sending message:', err);
        this.messages[botIdx] = {
          text: 'Error: Could not get response',
          isUser: false
        };
        this.isSending = false;
      }
    });
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
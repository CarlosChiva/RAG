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

  // chat.component.ts (o el archivo que contenga sendMessage)
// chat.component.ts
sendMessage(messageFromChild?: string): void {
  const messageText = messageFromChild || this.message || this.currentMessage;

  if (!messageText.trim() || !this.selectedConfig) {
    alert('Please enter a message and select a collection.');
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
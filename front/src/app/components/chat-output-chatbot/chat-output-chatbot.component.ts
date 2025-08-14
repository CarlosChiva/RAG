// chat-output-chatbot.component.ts - Versión completa
import { Component, Input, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface ChatMessage {
  text: string | Promise<string> | any; // SafeHtml from DomSanitizer
  isUser: boolean;
  isTyping?: boolean;
  eventHeader?: string;
  tokens?: string[];
  showThinking?: boolean;
  thinkingTokens?: string[];
  responseText?: string | any; // SafeHtml from DomSanitizer
    eventHistory?: string[];  // AÑADIR ESTA LÍNEA
  currentEvent?: string;    // AÑADIR ESTA LÍNEA (opcional, por si la usas después)
}

@Component({
  selector: 'app-chat-output-chatbot',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './chat-output-chatbot.component.html',
  styleUrls: ['./chat-output-chatbot.component.scss']
})
export class ChatOutputChatbotComponent implements AfterViewChecked {
  @Input() messages: ChatMessage[] = [];
  @Input() showTables: boolean = false; // Por compatibilidad con el template padre
  @ViewChild('chatOutput') chatOutput!: ElementRef;

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      if (this.chatOutput && this.chatOutput.nativeElement) {
        this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
      }
    } catch(err) {
      console.warn('Error scrolling to bottom:', err);
    }
  }

  public getChatOutputElement(): ElementRef {
    return this.chatOutput;
  }

  // Método para alternar la visibilidad del contenido de thinking
  toggleThinking(messageIndex: number): void {
    if (this.messages[messageIndex]) {
      this.messages[messageIndex].showThinking = !this.messages[messageIndex].showThinking;
    }
  }

  // Método auxiliar para verificar si un mensaje tiene tokens de thinking
  hasThinkingTokens(message: ChatMessage): boolean {
    return !!(message.thinkingTokens && message.thinkingTokens.length > 0);
  }

  // Método auxiliar para contar tokens de thinking
  getThinkingTokensCount(message: ChatMessage): number {
    return message.thinkingTokens ? message.thinkingTokens.length : 0;
  }
}
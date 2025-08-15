import { SafeHtml } from "@angular/platform-browser";

export interface ChatMessage {
  text: string | Promise<string> | SafeHtml;
  isUser: boolean;
  isTyping?: boolean;
  eventHeader?: string;
  thinkingTokens?: string[];
  responseText?: string | SafeHtml;
  showThinking?: boolean;
  eventHistory?: string[];  // NUEVO: historial de eventos
  currentEvent?: string;    // NUEVO: evento actual
}
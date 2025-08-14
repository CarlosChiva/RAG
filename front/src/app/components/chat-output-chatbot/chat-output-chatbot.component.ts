// chat-output.component.ts
import { Component, Input, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat-output-chatbot',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './chat-output-chatbot.component.html',
  styleUrls: ['./chat-output-chatbot.component.scss']
})
export class ChatOutputChatbotComponent implements AfterViewChecked {
  @Input() messages: any[] = [];
  
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  
  ngAfterViewChecked() {
    this.scrollToBottom();
  }
  
  scrollToBottom(): void {
    try {
      this.chatOutput.nativeElement.scrollTop = this.chatOutput.nativeElement.scrollHeight;
    } catch(err) { }
  }
  
  // Método para acceder al elemento nativo si es necesario
  public getChatOutputElement(): ElementRef {
    return this.chatOutput;
  }
}
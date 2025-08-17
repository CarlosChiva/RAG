import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common'; 
@Component({
  selector: 'app-user-input-chatbot',
  imports: [CommonModule],
  templateUrl: './user-input.component-chatbot.html',
  styleUrl: './user-input.component-chatbot.scss'
})
export class UserInputChatbotComponent {
@Input() placeholder: string = 'Type your message here...';
  @Input() isSending: boolean = false;
  @Input() disabled: boolean = false;
  @Input() sendButtonText: string = 'Send';
  
  @Output() messageChange = new EventEmitter<string>();
  @Output() sendMessage = new EventEmitter<string>();

  private _message: string = '';

  @Input() 
  get message(): string {
    return this._message;
  }

  set message(value: string) {
    this._message = value;
    this.messageChange.emit(value);
  }

  onInputChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.message = target.value;
  }

  onSendMessage(): void {
    if (this._message.trim() && !this.isSending && !this.disabled) {
      this.sendMessage.emit(this._message);
    }
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.onSendMessage();
    }
  }
}
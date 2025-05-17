// chat-output.component.ts
import { Component, Input, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TablaComponent } from '../tabla/tabla.component';

@Component({
  selector: 'app-chat-output',
  standalone: true,
  imports: [CommonModule, TablaComponent],
  templateUrl: './chat-output.component.html',
  styleUrls: ['./chat-output.component.scss']
})
export class ChatOutputComponent implements AfterViewChecked {
  @Input() messages: any[] = [];
  @Input() showTables: boolean = false;
  
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
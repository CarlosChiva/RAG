import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from '../../components/upload_pdf/upload_pdf.component';
import { ChatOutputComponent } from '../../components/chat-output/chat-output.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ExcelService } from '../../services/excel.service';
import { Router, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarItemComponent } from '../../components/sidebar-pdf-item/sidebar-pdf-item.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';

@Component({
  selector: 'app-excels',
  imports: [
    HttpClientModule,
    CommonModule,
    UploadComponent,
    SidebarComponent,
    SidebarItemComponent,
    ChatOutputComponent,
    ButtonContainerComponent,
    UserInputComponent
  ],
  templateUrl: './excels.component.html',
  styleUrl: './excels.component.scss'
})
export class Excels implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;
  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarItemComponent) sidebarItemComponent!: SidebarItemComponent;

  // Properties from template
  collections: any[] = [];
  selectedCollection: any = null;
  messages: any[] = [];
  isSending: boolean = false;
  currentMessage: string = '';
  sidebarCollapsed: boolean = false;
  mostrarModal: boolean = false;
  files: string[] = [];

  constructor(
    private configsService: ExcelService,
    private router: Router,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.loadConfigs();
  }

  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  loadConfigs(): void {
    this.configsService.listFiles().subscribe({
      next: (response: any) => {
        this.files = response.files;
        console.log(this.files)
        // if (this.collections.length === 0) {
        //   this.abrirModal();
        // }
      },
      error: (error: any) => console.error('Error fetching collections:', error)
    });
  }

  selectCollection(collection: any): void {
    this.selectedCollection = collection;
  }

  renderConversation(conversation: any): void {
    // Handle conversation loading
  }

  deleteCollection(collection: any): void {
    // Handle collection deletion
  }

  onMessageChange(message: string): void {
    this.currentMessage = message;
  }

  sendMessage(message: string): void {
    if (!message.trim() || !this.selectedCollection) return;
    
    this.isSending = true;
    // Here you would typically send the message to your backend
    // and handle the response
    this.isSending = false;
  }

  abrirModal(): void {
    this.mostrarModal = true;
  }

  cerrarModal(): void {
    this.mostrarModal = false;
  }
}

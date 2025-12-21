import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatOutputComponent } from '../../components/chat-output/chat-output.component';
import { ButtonContainerComponent } from '../../components/button-container/button-container.component';
import { ExcelService } from '../../services/excel.service';
import { Router, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { SidebarExcelItemComponent } from '../../components/sidebar-excel-item/sidebar-excel-item.component';
import { UserInputComponent } from '../../components/user-input/user-input.component';
import { ExcelUploaderComponent } from '../../components/excel-uploader/excel-uploader.component';

@Component({
  selector: 'app-excels',
  imports: [
    HttpClientModule,
    CommonModule,
    SidebarComponent,
    
    SidebarExcelItemComponent,
    ChatOutputComponent,
    ButtonContainerComponent,
    UserInputComponent,
    ExcelUploaderComponent
  ],
  templateUrl: './excels.component.html',
  styleUrl: './excels.component.scss'
})
export class Excels implements OnInit {
  @ViewChild('chatOutput') chatOutput!: ElementRef;
  @ViewChild('inputText') inputText!: ElementRef;
  @ViewChild(ChatOutputComponent) chatOutputComponent!: ChatOutputComponent;
  @ViewChild(SidebarComponent) sidebarComponent!: SidebarComponent;
  @ViewChild(SidebarExcelItemComponent) sidebarItem!: SidebarExcelItemComponent;

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
        // Open modal if no files are available
        if (this.files.length === 0) {
          this.abrirModal();
        }
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
    // Remove the collection from the files array
    this.files = this.files.filter(file => file !== collection);
    // Optionally, if the deleted collection was selected, deselect it
    if (this.selectedCollection === collection) {
      this.selectedCollection = null;
    }
    // Check if we need to open the modal when there are no files left
    if (this.files.length === 0) {
      this.abrirModal();
    }
  }

  toggleShowFile(file: string): void {
    // Handle file show/hide toggle
    console.log('Toggle show for file:', file);
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
    // Reload files after closing the modal (to show newly uploaded files)
    this.loadConfigs();
  }

  onFileUploaded(): void {
    // This method is called when a file is successfully uploaded
    // Reload the file list to show the new file
    this.loadConfigs();
  }
}

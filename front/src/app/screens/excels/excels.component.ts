import { Component, OnInit,ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UploadComponent } from '../../components/upload_pdf/upload_pdf.component'; // Importar componente
import {ChatOutputComponent} from '../../components/chat-output/chat-output.component';
import {ButtonContainerComponent} from '../../components/button-container/button-container.component';

import {SidebarComponent} from '../../components/sidebar/sidebar.component';
import {SidebarItemComponent} from '../../components/sidebar-pdf-item/sidebar-pdf-item.component';
import {UserInputComponent} from '../../components/user-input/user-input.component';

@Component({
  selector: 'app-excels',
  imports: [CommonModule,UploadComponent,SidebarComponent,SidebarItemComponent,ChatOutputComponent,ButtonContainerComponent,UserInputComponent],
  templateUrl: './excels.component.html',
  styleUrl: './excels.component.scss',
})
export class Excels implements OnInit{
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

  ngOnInit(): void {
    // Initialize any data if needed
  }

  // Methods from template event handlers
  selectCollection(collection: any): void {
    this.selectedCollection = collection;
    // You might want to load the collection data here
  }

  renderConversation(conversation: any): void {
    // Handle conversation loading
  }

  deleteCollection(collection: any): void {
    // Handle collection deletion
  }

  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
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

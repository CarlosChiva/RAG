import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common'; // Añade esta importación
import { FormsModule } from '@angular/forms';  // Importa FormsModule para ngModel
import { ModelsService } from '../../services/models.service';

@Component({
  selector: 'app-sidebar-conversations-item',
  imports: [CommonModule, FormsModule],  // Añade FormsModule aquí
  templateUrl: './sidebar-conversations-item.component.html',
  styleUrls: ['./sidebar-conversations-item.component.scss']
})
export class SidebarItemComponent {
  @Input() collection : string | null= null;
  @Input() isSelected: boolean = false;
  @Input() displayField: string = '';

  @Output() selectItem = new EventEmitter<any>();
  @Output() deleteItem = new EventEmitter<any>();
  @Output() itemDeleted = new EventEmitter<any>();
  @Output() conversationLoaded = new EventEmitter<any[]>();

  editing: boolean = false;
  newCollectionName: string = '';

  constructor(private modelsService: ModelsService) {}

  getDisplayValue(): string {
    if (!this.collection) return '';
    // Si es un objeto DbConfig
    return this.collection;
  }

  onSelect(): void {
    if (this.collection) {
      this.selectItem.emit(this.collection);
      // Obtenemos la conversación desde el servicio
      this.modelsService.getConversation(this.collection).subscribe({
        next: (conversation) => {
          console.log('Conversation loaded:', conversation);
          this.conversationLoaded.emit(conversation);
        },
        error: (err) => {
          console.error('Error loading conversation:', err);
        }
      });
    }
  }

  onDelete(event: Event): void {
    event.stopPropagation();
    this.modelsService.removeChat(this.collection as string).subscribe({
      next: () => {
        console.log('Configuration deleted:', this.collection);
        alert('Collection deleted successfully');
        this.itemDeleted.emit(this.collection);
      },
      error: (error) => {
        console.error('Error deleting configuration:', error);
        alert('Error deleting configuration');
      }
   });
  }

  toggleEdit(event: Event): void {
    event.stopPropagation();
    if (this.editing) {
      // Si ya está en modo edición, guarda los cambios
      this.saveEdit();
    } else {
      // Entra en modo edición
      this.newCollectionName = this.collection || '';
      this.editing = true;
    }
  }

  saveEdit(): void {
    this.editing = false;

    if (this.newCollectionName && this.newCollectionName !== this.collection) {
      this.modelsService.updateChatName(this.collection as string, this.newCollectionName).subscribe({
        next: () => {
          console.log('Collection renamed:', this.newCollectionName);
          alert('Collection renamed successfully');
          // Actualiza el nombre de la colección
          this.collection = this.newCollectionName;
        },
        error: (error) => {
          console.error('Error renaming collection:', error);
          alert('Error renaming collection');
        }
      });
    }

    // Sale del modo edición
    this.editing = false;
  }
}
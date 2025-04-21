import { Component, Input, Output, EventEmitter } from '@angular/core';

import { CommonModule } from '@angular/common'; // Añade esta importación
import {CollectionsService} from '../../services/collections.service';  
@Component({
  selector: 'app-sidebar-item',
  imports: [CommonModule],
  templateUrl: './sidebar-pdf-item.component.html',
  styleUrl: './sidebar-pdf-item.component.scss'
})
export class SidebarItemComponent {
  @Input() collection : string | null= null;
  @Input() isSelected: boolean = false;
  @Input() displayField: string = '';

  
  @Output() selectItem = new EventEmitter<any>();
  @Output() deleteItem = new EventEmitter<any>();
  @Output() itemDeleted = new EventEmitter<any>();

  constructor(private collectionService:CollectionsService){}
  
  getDisplayValue(): string {
    if (!this.collection) return '';
    
    // Si es un objeto DbConfig
    return this.collection;
  }

  onSelect(): void {
    if (this.collection) {
      this.selectItem.emit(this.collection);
    }
  }

  onDelete(event: Event): void {
    event.stopPropagation();
    this.collectionService.deleteCollection(this.collection as string).subscribe({
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


}
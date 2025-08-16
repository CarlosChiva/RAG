import { Component, Input, Output, EventEmitter } from '@angular/core';
import {DdbbServices} from '../../services/ddbb.service';
import {DbConfig} from '../../interfaces/db-conf.interface';
import { CommonModule } from '@angular/common'; // Añade esta importación

@Component({
  selector: 'app-ddbb-sidebar-item',
  imports: [CommonModule],
  templateUrl: './sidebar-ddbb-item.component.html',
  styleUrl: './sidebar-ddbb-item.component.scss'
})
export class SidebarItemComponent {
  @Input() item!: DbConfig | string;
  @Input() isSelected: boolean = false;
  @Input() displayField: string = '';
  @Input() showEditButton: boolean = false;
  
  @Output() selectItem = new EventEmitter<any>();
  @Output() editItem = new EventEmitter<any>();
  @Output() deleteItem = new EventEmitter<any>();
  @Output() itemDeleted = new EventEmitter<any>();
  @Output() connectionError = new EventEmitter<string>();
  @Output() openModal = new EventEmitter<DbConfig>(); // cambio aquí

  constructor(private configsService: DdbbServices) {}
  
  getDisplayValue(): string {
    if (!this.item) return '';
    
    // Si es un string
    if (typeof this.item === 'string') {
      return this.item;
    }
    
    // Si es un objeto DbConfig
    return this.item.connection_name;
  }

  onSelect(): void {
      // Solo procesamos la selección si es un objeto DbConfig
      if (typeof this.item !== 'string') {
        // Verificamos la conexión antes de emitir el evento de selección
        this.configsService.tryConnection(this.item).subscribe({
          next: (response: boolean) => {
            if (response) {
              // Conexión exitosa, emitimos el evento de selección
              this.selectItem.emit(this.item);
            } else {
              console.log("Conexión fallida");
              alert("No se pudo conectar a la base de datos.");
              // Opcionalmente, puedes emitir un evento de error
              this.connectionError.emit("No se pudo conectar a la base de datos.");
              this.selectItem.emit(null);
            }
          },
          error: (error) => {
            const backendError = error?.error?.detail;
            console.error("Error de conexión:", error);
            alert(`❌ Error: ${backendError}`);
            // Emitir el error para que el componente padre pueda manejarlo si es necesario
            this.connectionError.emit(backendError || "Error de conexión");
          }
        });
      } else {
        // Si es un string, simplemente emitimos el evento sin verificar conexión
        this.selectItem.emit(this.item);
      }
    }


  onDelete(event: Event): void {
    event.stopPropagation();
    
    // Verificar si item es DbConfig
    if (typeof this.item !== 'string') {
      this.configsService.removeConfig(this.item).subscribe({
        next: () => {
          console.log('Configuration deleted:', this.item);
          alert('Configuration deleted successfully');
          this.itemDeleted.emit(this.item);
        },
        error: (error) => {
          console.error('Error deleting configuration:', error);
          alert('Error deleting configuration');
        }
      });
    } else {
      console.error('Cannot delete a string item');
      alert('Error: Cannot delete this item');
    }
  }
  // Método para abrir el modal de edición
  onEdit(event: Event): void {
    event.stopPropagation(); // Evita que se active la selección del item
    
    if (typeof this.item !== 'string') {
      this.openModal.emit(this.item as DbConfig);
    } else {
      console.error('Cannot edit a string item');
      alert('Error: Cannot edit this item');
    }
  }

}
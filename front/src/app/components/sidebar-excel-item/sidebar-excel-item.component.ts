import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExcelService } from '../../services/excel.service';

@Component({
  selector: 'app-sidebar-excel-item',
  imports: [CommonModule],
  templateUrl: './sidebar-excel-item.component.html',
  styleUrls: ['./sidebar-excel-item.component.scss']
})
export class SidebarExcelItemComponent {
  @Input() itemName: string = '';
  @Input() isShown: boolean = true;
  @Input() isSelected: boolean = false;

  @Output() deleteItem = new EventEmitter<string>();
  @Output() toggleShow = new EventEmitter<string>();
  @Output() selectItem = new EventEmitter<string>();

  constructor(private excelService: ExcelService) {}

  onDelete(): void {
    this.deleteItem.emit(this.itemName);
    // Eliminar el archivo del backend primero
    this.excelService.deleteFile(this.itemName).subscribe({
      next: () => {
        console.log(`File ${this.itemName} deleted successfully`);
        // No recargar aquí, el padre se encargará de actualizar la lista
      },
      error: (err: any) => {
        console.error(`Error deleting file ${this.itemName}:`, err);
        // Opcionalmente mostrar notificación de error
      }
    });
  }

  onToggleShow(): void {
    this.toggleShow.emit(this.itemName);
  }

  onSelect(): void {
    this.selectItem.emit(this.itemName);
  }
}

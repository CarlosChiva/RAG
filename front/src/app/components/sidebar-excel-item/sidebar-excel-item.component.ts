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
    this.excelService.deleteFile(this.itemName).subscribe({
      next: () => {
        console.log(`File ${this.itemName} deleted successfully`);
        // Optionally refresh the file list or show a notification
      },
      error: (err) => {
        console.error(`Error deleting file ${this.itemName}:`, err);
        // Optionally show an error notification
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

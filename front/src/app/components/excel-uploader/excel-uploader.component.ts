import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-excel-uploader',
  standalone: true,
  imports: [],
  templateUrl: './excel-uploader.component.html',
  styleUrls: ['./excel-uploader.component.scss']
})
export class ExcelUploaderComponent implements OnInit {
  @Output() cerrarModal = new EventEmitter<void>();

  selectedFileName: string | null = null;

  ngOnInit(): void {}

  onSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (this.isValidFile(file)) {
        this.selectedFileName = file.name;
        // Close modal after successful selection
        this.cerrarModal.emit();
      } else {
        alert('Solo se permiten archivos .xlsx');
      }
    }
  }

  private isValidFile(file: File): boolean {
    return file.name.endsWith('.xlsx');
  }
}

import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ExcelService } from '../../services/excel.service';

@Component({
  selector: 'app-excel-uploader',
  standalone: true,
  imports: [],
  templateUrl: './excel-uploader.component.html',
  styleUrls: ['./excel-uploader.component.scss']
})
export class ExcelUploaderComponent implements OnInit {
  @Output() cerrarModal = new EventEmitter<void>();
  @Output() fileUploaded = new EventEmitter<void>();

  selectedFileName: string | null = null;
  isDragOver: boolean = false;

  constructor(private excelService: ExcelService) {}

  ngOnInit(): void {}

  onSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (this.isValidFile(file)) {
        this.selectedFileName = file.name;
        this.uploadFile(file);
      } else {
        alert('Solo se permiten archivos .xlsx');
      }
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragOver = false;
    
    if (event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      if (this.isValidFile(file)) {
        this.selectedFileName = file.name;
        this.uploadFile(file);
      } else {
        alert('Solo se permiten archivos .xlsx');
      }
    }
  }

  private isValidFile(file: File): boolean {
    return file.name.endsWith('.xlsx');
  }

  private uploadFile(file: File): void {
    this.excelService.uploadFile(file).subscribe({
      next: (response) => {
        console.log('File uploaded successfully', response);
        // Emit event to parent component
        this.fileUploaded.emit();
        // Close modal after successful upload
        this.cerrarModal.emit();
      },
      error: (error) => {
        console.error('Error uploading file', error);
        alert('Error al subir el archivo');
      }
    });
  }
}

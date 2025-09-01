import { Component, ElementRef, Output, EventEmitter, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ModelsService } from '../../services/models.service';

@Component({
  selector: 'app-upload-mcp',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './upload_mcp.component.html',
  styleUrls: ['./upload_mcp.component.scss'],
})
export class UploadMCPComponent {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  @ViewChild('jsonTextarea') jsonTextarea!: ElementRef<HTMLTextAreaElement>;

  @Output() cerrarMCPModal = new EventEmitter<void>();

  isLoading = false;
  file: File | null = null;
  jsonInput = '';        // holds raw JSON string (file‑loaded or manually typed)
  useFile = true;        // mode: true = file, false = write
  showPreview = false;   // show textarea after file is loaded

  constructor(private router: Router, private modelsService: ModelsService) {}

  /* ----------  Toggle mode (checkbox)  ---------- */
  onUseFileChange(): void {
    if (!this.useFile) {
      // user switched to “write JSON” mode – clear everything
      this.file = null;
      this.jsonInput = '';
      this.showPreview = false;
    } else {
      // user switched to “file upload” mode – if a file is already selected, read it
      if (this.file) this.readFile(this.file);
    }
  }

  /* ----------  File / Drag‑Drop helpers  ---------- */
  openFileDialog(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.file = input.files[0];
      this.readFile(this.file);
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropzone = event.currentTarget as HTMLElement;
    dropzone.classList.add('dragover');
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropzone = event.currentTarget as HTMLElement;
    dropzone.classList.remove('dragover');
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropzone = event.currentTarget as HTMLElement;
    dropzone.classList.remove('dragover');

    // 1️⃣ Check if a file was dropped
    const files = event.dataTransfer?.files;
    if (files && files.length) {
      this.file = files[0];
      this.readFile(this.file);
      return;
    }

    // 2️⃣ No file – maybe plain text was dropped
    const text = event.dataTransfer?.getData('text/plain');
    if (text) {
      this.jsonInput = text.trim();
      this.file = null;
      this.showPreview = true;
    }
  }

  /* ----------  Read file into jsonInput  ---------- */
  private readFile(file: File): void {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        this.jsonInput = reader.result;
        this.showPreview = true;
      }
    };
    reader.onerror = () => {
      alert('Error reading the file.');
      this.isLoading = false;
    };
    reader.readAsText(file);
  }

  /* ----------  Upload logic  ---------- */
  uploadFiles(): void {
    if (!this.jsonInput.trim()) {
      alert('Please provide a JSON file or paste JSON text.');
      return;
    }



    // Validate JSON before sending
    let parsed: any;
    try {
      parsed = JSON.parse(this.jsonInput);
    } catch (err) {
      alert('The provided text is not valid JSON.');
      return;
    }

    const inner = parsed.comfyuiConf ?? parsed;
    const combinedConfig = {
      mcp_tools: {
        api_json: inner,
      },
    };

    this.isLoading = true;
    this.modelsService.updateToolsConf(combinedConfig).subscribe({
      next: () => alert('Files uploaded successfully!'),
      error: (err) => alert(err.error?.error || 'Error uploading files.'),
      complete: () => (this.isLoading = false),
    });
  }

  /* ----------  Close modal  ---------- */
  cerrar(): void {
    this.cerrarMCPModal.emit();
  }
}
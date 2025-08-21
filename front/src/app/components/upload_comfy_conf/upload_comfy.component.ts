// upload.component.ts
import { Component, OnInit, ViewChild, ElementRef, Output, EventEmitter } from '@angular/core';
import { Router} from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CollectionsService } from '../../services/collections.service';

@Component({
  selector: 'app-upload-Comfy',
  standalone: true,
  imports: [CommonModule, HttpClientModule,  FormsModule],
  templateUrl: './upload_comfy.component.html',
  styleUrls: ['./upload_comfy.component.scss']
})
export class UploadComfyComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  @Output() cerrarModal = new EventEmitter<void>(); // Evento para cerrar el modal

  collections: string[] = [];
  selectedCollection: string = '';
  newCollection: string = '';
  isLoading: boolean = false;
  files: FileList | null = null;

  constructor(
    private router: Router,
    private collectionsService: CollectionsService

  ) {}

  ngOnInit(): void {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      alert('Token expired. Please, sign up again');
      this.router.navigate(['/login']);
      return;
    }
    
    this.loadCollections();
  }

  loadCollections(): void {
    this.collectionsService.getCollections().subscribe({
      next: (data) => {
        this.collections = data.collections_name;
      },
      error: (error) => console.error('Error fetching collections:', error)
    });
  }

  openFileDialog(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.files = input.files;
    }
  }

  navigateBack(): void {
    this.collectionsService.getCollections().subscribe({
      next: (data) => {
        if (data.collections_name.length === 0) {
          alert('No collections found');
          this.router.navigate(['/menu']);
        } else {
          this.router.navigate(['/pdf']);
        }
      },
      error: (error) => {
        console.error('Error fetching collections:', error);
      }
    });
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
    
    if (event.dataTransfer?.files) {
      this.files = event.dataTransfer.files;
    }
  }

  uploadFiles(): void {
    if (!this.files || this.files.length === 0) {
      alert('Please select a file.');
      return;
    }

    if (!this.selectedCollection && !this.newCollection) {
      alert('Please select an existing collection or create a new one.');
      return;
    }

    // Definir correctamente la variable collectionName
    const collectionToUse = this.selectedCollection || this.newCollection;
       
    this.isLoading = true;
    
    this.collectionsService.uploadFiles(this.files, collectionToUse).subscribe({
      next: (response: any) => {
        alert('Files uploaded successfully!');
        this.files = null;
        this.selectedCollection = '';
        this.newCollection = '';
        if (this.fileInput.nativeElement) {
          this.fileInput.nativeElement.value = '';
        }
      },
      error: (error) => {
        alert(error.error?.error || 'Error uploading files.');
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }
  cerrar() {
    this.cerrarModal.emit(); // Notifica al componente padre que cierre la ventana emergente
  }
}
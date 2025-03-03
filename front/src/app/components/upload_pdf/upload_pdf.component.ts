// upload.component.ts
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router} from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, HttpClientModule,  FormsModule],
  templateUrl: './upload_pdf.component.html',
  styleUrls: ['./upload_pdf.component.scss']
})
export class UploadComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  
  collections: string[] = [];
  selectedCollection: string = '';
  newCollection: string = '';
  isLoading: boolean = false;
  files: FileList | null = null;

  constructor(
    private router: Router,
    private http: HttpClient
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
    const token = localStorage.getItem('access_token');
    
    this.http.get<{collections_name: string[]}>('http://127.0.0.1:8000/collections', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    }).subscribe({
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
    const token = localStorage.getItem('access_token');
    
    this.http.get<{collections_name: string[]}>('http://127.0.0.1:8000/collections', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    }).subscribe({
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

    const token = localStorage.getItem('access_token');
    const formData = new FormData();
    
    for (let i = 0; i < this.files.length; i++) {
      formData.append('file', this.files[i]);
    }
    
    formData.append('name_collection', this.selectedCollection || this.newCollection);
    
    this.isLoading = true;
    
    this.http.post('http://localhost:8000/add_document', formData, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    }).subscribe({
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
}
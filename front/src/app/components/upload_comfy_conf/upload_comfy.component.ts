// upload.component.ts
import { Component, OnInit, ViewChild, ElementRef, Output, EventEmitter } from '@angular/core';
import { Router} from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ModelsService } from '../../services/models.service';

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
  positivePromptNode: string = '';
  isLoading: boolean = false;
  file: File | null = null;

  constructor(
    private router: Router,
    private modelsService: ModelsService

  ) {}

  ngOnInit(): void {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      alert('Token expired. Please, sign up again');
      this.router.navigate(['/login']);
      return;
    }
    
  }


  openFileDialog(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
      // Si el input contiene archivos
    if (input.files && input.files.length > 0) {
    // Tomamos el **primer** (y único) archivo
      this.file = input.files[0];
    }
  }

  navigateBack(): void {
  
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
    const fileList = event.dataTransfer?.files;

    if (fileList && fileList.length > 0) {
      this.file = fileList[0];
    }
  }

  uploadFiles(): void {
    if (!this.file ) {
      alert('Please select a file.');
      return;
    }

    if (!this.positivePromptNode) {
      alert('Please select an existing collection or create a new one.');
      return;
    }
    let combinedConfig: any = null;
    let newComfyuiConf: any = { positive_prompt_node: this.positivePromptNode };

       
    const reader = new FileReader();

    reader.onload = () => {
      try {
        // ---- 2️⃣  Parsear el contenido JSON ----
        const fileContent = reader.result as string;
        const parsed = JSON.parse(fileContent);

        // ---- 3️⃣  Extraer la sección “comfyuiConf” ----
        // Si el JSON ya viene sin ese wrapper, usamos `parsed` directamente.
        const inner = parsed.comfyuiConf ?? parsed;

        // ---- 4️⃣  Fusionar con newComfyuiConf ----
        combinedConfig = { ...inner, ...newComfyuiConf };

        // --------- 5️⃣  Hacer lo que necesites con la configuración ----------
        console.log('Configuración combinada:', combinedConfig);
        // Por ejemplo, guardarla en un servicio, enviarla a un API, etc.
      } catch (err) {
        console.error(err);
        alert('El archivo no es un JSON válido o tiene un formato inesperado.');
      } finally {
        this.isLoading = false;
      }
    };

    reader.onerror = () => {
      console.error('Error al leer el archivo.');
      alert('Error al leer el archivo.');
      this.isLoading = false;
    };

    // ---- 6️⃣  Iniciar la lectura como texto ----
    reader.readAsText(this.file);
  




    this.isLoading = true;
    
    this.modelsService.updateComfyUiConf(combinedConfig).subscribe({
      next: (response: any) => {
        alert('Files uploaded successfully!');
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
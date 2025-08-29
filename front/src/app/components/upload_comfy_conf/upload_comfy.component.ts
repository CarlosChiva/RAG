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
  if (!this.file) {
    alert('Please select a file.');
    return;
  }
  if (!this.positivePromptNode) {
    alert('Please select an existing collection or create a new one.');
    return;
  }

  const reader = new FileReader();

  reader.onload = () => {
    try {
      const fileContent = reader.result as string;
      const parsed = JSON.parse(fileContent);

      // Si el JSON ya no tiene la clave 'comfyuiConf', usamos el objeto completo
      const inner = parsed.comfyuiConf ?? parsed;

      // Fusionamos con el nodo positivo
      const combinedConfig = {
        image_tools:{
          api_json: inner,
          positive_prompt_node: this.positivePromptNode,
        }
      };

      console.log('Configuración combinada:', combinedConfig);

      // Ahora sí enviamos la configuración
      this.isLoading = true;
      this.modelsService.updateToolsConf(combinedConfig).subscribe({
        next: (_) => alert('Files uploaded successfully!'),
        error: (err) => alert(err.error?.error || 'Error uploading files.'),
        complete: () => this.isLoading = false,
      });

    } catch (err) {
      console.error(err);
      alert('El archivo no es un JSON válido o tiene un formato inesperado.');
      this.isLoading = false;
    }
  };

  reader.onerror = () => {
    console.error('Error al leer el archivo.');
    alert('Error al leer el archivo.');
    this.isLoading = false;
  };

  // Inicia la lectura
  reader.readAsText(this.file);
}
  cerrar() {
    this.cerrarModal.emit(); // Notifica al componente padre que cierre la ventana emergente
  }
}
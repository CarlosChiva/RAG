// upload.component.ts
import { Component, OnInit, ViewChild, ElementRef, Output, EventEmitter, Input } from '@angular/core';
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
  @ViewChild('jsonTextarea') jsonTextarea!: ElementRef<HTMLTextAreaElement>;
  @Output() cerrarImageModal = new EventEmitter<void>(); // Evento para cerrar el modal
  @Input() editConfig: any = null; // Nueva propiedad para recibir la config

  collections: string[] = [];
  positivePromptNode: string = '';
  isLoading: boolean = false;
  file: File | null = null;
  
  // Nuevas propiedades para el modo de entrada
  useFile: boolean = true;        // true = usar archivo, false = escribir JSON
  jsonInput: string = '';         // contenido del JSON (desde archivo o escrito)
  showPreview: boolean = false;   // mostrar textarea después de cargar archivo
  isEditMode: boolean = false;    // para saber si estamos en modo edición

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

    // Si hay configuración para editar, cargarla
    if (this.editConfig) {
      this.isEditMode = true;
      this.jsonInput = JSON.stringify(this.editConfig.api_json || this.editConfig, null, 2);
      this.positivePromptNode = this.editConfig.positive_prompt_node || '';
      this.showPreview = true;
      this.useFile = false; // Mostrar directamente el textarea
    }
  }

  /* ----------  Toggle mode (checkbox)  ---------- */
  onUseFileChange(): void {
    if (!this.useFile) {
      // usuario cambió a modo "escribir JSON" – limpiar todo
      this.file = null;
      this.jsonInput = '';
      this.showPreview = false;
    } else {
      // usuario cambió a modo "subir archivo" – si ya hay un archivo seleccionado, leerlo
      if (this.file) {
        this.readFile(this.file);
      }
    }
  }

  openFileDialog(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.file = input.files[0];
      this.readFile(this.file);
    }
  }

  /* ----------  Drag & Drop  ---------- */
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

    // 1️⃣ Verificar si se soltó un archivo
    const files = event.dataTransfer?.files;
    if (files && files.length) {
      this.file = files[0];
      this.readFile(this.file);
      return;
    }

    // 2️⃣ No hay archivo – tal vez se soltó texto plano
    const text = event.dataTransfer?.getData('text/plain');
    if (text) {
      this.jsonInput = text.trim();
      this.file = null;
      this.showPreview = true;
    }
  }

  /* ----------  Leer archivo a jsonInput  ---------- */
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

  uploadFiles(): void {
    // Validar que hay contenido JSON
    if (!this.jsonInput.trim()) {
      alert('Please provide a JSON file or paste JSON text.');
      return;
    }

    if (!this.positivePromptNode) {
      alert('Please enter the positive prompt node number.');
      return;
    }

    // Validar JSON antes de enviar
    let parsed: any;
    try {
      parsed = JSON.parse(this.jsonInput);
    } catch (err) {
      alert('The provided text is not valid JSON.');
      return;
    }

    // Si el JSON ya no tiene la clave 'comfyuiConf', usamos el objeto completo
    const inner = parsed.comfyuiConf ?? parsed;

    // Fusionamos con el nodo positivo
    const combinedConfig = {
      image_tools: {
        api_json: inner,
        positive_prompt_node: this.positivePromptNode,
      }
    };

    console.log('Configuración combinada:', combinedConfig);

    // Enviar la configuración
    this.isLoading = true;
    this.modelsService.updateToolsConf(combinedConfig).subscribe({
      next: (_) => alert('Configuration uploaded successfully!'),
      error: (err) => alert(err.error?.error || 'Error uploading configuration.'),
      complete: () => this.isLoading = false,
    });
  }

  cerrar() {
    this.cerrarImageModal.emit(); // Notifica al componente padre que cierre la ventana emergente
  }
}
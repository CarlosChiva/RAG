import { Component, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { ModelsService } from '../../services/models.service';

@Component({
  selector: 'app-user-input-chatbot',
  imports: [CommonModule],
  templateUrl: './user-input.component-chatbot.html',
  styleUrl: './user-input.component-chatbot.scss'
})
export class UserInputChatbotComponent implements OnInit {
 
  @Input() placeholder: string = 'Type your message here...';
  @Input() isSending: boolean = false;
  @Input() disabled: boolean = false;
  @Input() sendButtonText: string = 'Send';
  
  @Output() messageChange = new EventEmitter<string>();
  @Output() sendMessage = new EventEmitter<string>();
  @Output() toolConfigSelected = new EventEmitter<any>();

  dropdownDirection: 'up' | 'down' = 'down';
  toolSelected: string | null = null;
  mcp_conf:Object={};
  comfyui_conf:Object={};
  config_selected:Object={};
  private _message: string = '';
  constructor(private modelsService: ModelsService) {}  

  ngOnInit(): void {
        this.loadComfy();
  }
  // method to load comfyui configuration
  loadComfy() {
    this.modelsService.getToolsConf().subscribe({
      next: (data: any) => {
        const isEmptyObject = !data || Object.keys(data).length === 0;
        if (isEmptyObject){ 
          console.log("No se encontraron datos",data);
          return;
        }
        if ('image_tools' in data) {
          this.comfyui_conf = data.image_tools;
        } else if ('mcp_tools' in data) {
          this.mcp_conf = data.mcp_tools;
        }
        else{
          console.log("No se encontraron datos",data);
          return 
        }

      },
      error: (error) => console.error('Error fetching collections:', error)
    })
  }

  @Input() 
  get message(): string {
    return this._message;
  }

  set message(value: string) {
    this._message = value;
    this.messageChange.emit(value);
  }


  onInputChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.message = target.value;
  }
  
  onSendMessage(): void {
    if (this._message.trim() && !this.isSending && !this.disabled) {
      this.sendMessage.emit(this._message);
    }
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.onSendMessage();
    }
  }

    // Nuevas propiedades que necesitas agregar
  isToolSelected: boolean = false;
  isDropdownOpen: boolean = false;


    // Nuevos métodos que necesitas agregar
  toggleToolSelected(): void {
    this.isToolSelected = !this.isToolSelected;
    
    // Aquí puedes agregar tu lógica cuando se selecciona/deselecciona
    if (this.isToolSelected) {
      console.log('Image seleccionado');
      this.toolConfigSelected.emit(this.config_selected);
    } else  {
      console.log('Image deseleccionado');
      this.config_selected={};
    }
  }

  // Método para toggle del dropdown
  toggleDropdown(): void {
  this.isDropdownOpen = !this.isDropdownOpen;
  
  if (this.isDropdownOpen) {
    // Detectar si hay espacio suficiente abajo
    setTimeout(() => {
      const button = document.getElementById('dropdownButton');
      if (button) {
        const rect = button.getBoundingClientRect();
        const spaceBelow = window.innerHeight - rect.bottom;
        const spaceAbove = rect.top;
        const menuHeight = 120; // Altura estimada del menú (ajustar según necesites)
        
        this.dropdownDirection = spaceBelow >= menuHeight ? 'down' : 'up';
      }
    }, 0);
  }  }

  // Método para seleccionar una opción del dropdown
  selectOption(option: string): void {
    this.toolSelected = option;
    this.isDropdownOpen = false; // Cerrar el dropdown después de seleccionar

    if (option === 'image') {
      console.log('Seleccionaste Image');
      this.isToolSelected = true;
      this.config_selected = this.comfyui_conf;
      this.toolConfigSelected.emit(this.config_selected);

    } else if (option === 'mcp') {
      console.log('Seleccionaste MCP');
      this.config_selected = this.mcp_conf;
      this.isToolSelected = true;
      this.toolConfigSelected.emit(this.config_selected);

    }
  }

  // Opcional: Cerrar dropdown si se hace clic fuera del componente
  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    const target = event.target as HTMLElement;
    if (!target.closest('.dropdown-container')) {
      this.isDropdownOpen = false;
    }
  }
}
import { Component, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { ModelsService } from '../../services/models.service';
import {ToolConfigPayload } from '../../interfaces/config.interface';
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
  @Output() toolConfigSelected = new EventEmitter<ToolConfigPayload | null>();
  @Output() editToolConfig = new EventEmitter<string>();

  dropdownDirection: 'up' | 'down' = 'down';
  toolSelected: string | null = null;
  mcp_conf:Object={};
  comfyui_conf:Object={};
  config_selected:Object={};
  private _message: string = '';
  constructor(private modelsService: ModelsService) {}  

  ngOnInit():void {
      this.loadConfigs();
  }
    hasImageConfig(): boolean {
    return Object.keys(this.comfyui_conf).length > 0;
  }

  hasMcpConfig(): boolean {
    return Object.keys(this.mcp_conf).length > 0;
  }

  // method to load comfyui configuration

  loadConfigs() {
    this.modelsService.getToolsConf().subscribe({
      next: (data: any) => {
        console.log(data);
        const isEmptyObject = !data || Object.keys(data).length === 0;
        if (isEmptyObject){ 
          console.log("No se encontraron datos",data);
          return;
        }
        let data_json= data
        if ('image_tools' in data_json) {
          this.comfyui_conf = data_json.image_tools;
        }
        if ('mcp_tools' in data_json) {
          this.mcp_conf = data_json.mcp_tools;
        }
      // Debug: verificar que los métodos funcionen correctamente
      console.log('hasImageConfig():', this.hasImageConfig());
      console.log('hasMcpConfig():', this.hasMcpConfig());

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

 onEditTool(tool: string): void {
    // Emite el nombre del tool que se quiere editar
    this.editToolConfig.emit(tool);
    // Si quieres abrir directamente un modal, puedes hacerlo aquí.
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
    
    // // Aquí puedes agregar tu lógica cuando se selecciona/deselecciona
     if (this.isToolSelected) {
       console.log('Tool seleccionado');
 
     } else  {
       console.log('Tool deseleccionado');
       let playload={
        type:null,
        config:null
       }
       this.toolConfigSelected.emit(playload);
     }
  }

  // Método para toggle del dropdown
  toggleDropdown(): void {
    this.isDropdownOpen = !this.isDropdownOpen;
        // Debug: verificar que los métodos funcionen correctamente
      console.log('hasImageConfig():', this.hasImageConfig());
      console.log('hasMcpConfig():', this.hasMcpConfig());
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
    }
  }

  // Método para seleccionar una opción del dropdown
selectOption(option: string): void {
  this.toolSelected = option;
  this.isDropdownOpen = false; // close the dropdown

  let payload: ToolConfigPayload;
  console.log(this.comfyui_conf);
  console.log(this.mcp_conf);

  if (option === 'image') {
    console.log('Seleccionaste Image');
    this.isToolSelected = true;
    payload = { type: 'image', config: this.comfyui_conf };
  } else if (option === 'mcp') {
    console.log('Seleccionaste MCP',this.mcp_conf);
    this.isToolSelected = true;
    payload = { type: 'mcp', config: this.mcp_conf };
  } else {
    // unknown option – you could skip emission or send a default payload
    return;
  }

  this.toolConfigSelected.emit(payload);
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
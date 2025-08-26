import { Component, EventEmitter, HostListener, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common'; 
@Component({
  selector: 'app-user-input-chatbot',
  imports: [CommonModule],
  templateUrl: './user-input.component-chatbot.html',
  styleUrl: './user-input.component-chatbot.scss'
})
export class UserInputChatbotComponent {
@Input() placeholder: string = 'Type your message here...';
  @Input() isSending: boolean = false;
  @Input() disabled: boolean = false;
  @Input() sendButtonText: string = 'Send';
  
  @Output() messageChange = new EventEmitter<string>();
  @Output() sendMessage = new EventEmitter<string>();
  @Output() addComfyConfig = new EventEmitter<any>();
  @Input() comfyConfigExists: boolean = false;
  dropdownDirection: 'up' | 'down' = 'down';
  selectedOption: string | null = null;

  private _message: string = '';

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
  addConfig(event: Event): void {
    // Este método emite el evento hacia el padre sin importar qué botón se pulsó
    this.addComfyConfig.emit(event);
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
  toggleImageSelection(): void {
    this.isToolSelected = !this.isToolSelected;
    
    // Aquí puedes agregar tu lógica cuando se selecciona/deselecciona
    if (this.isToolSelected) {
      console.log('Image seleccionado');
      // Tu lógica para cuando está seleccionado
    } else {
      console.log('Image deseleccionado');
      // Tu lógica para cuando está deseleccionado
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
    this.selectedOption = option;
    this.isDropdownOpen = false; // Cerrar el dropdown después de seleccionar
    // Aquí puedes agregar tu lógica para manejar la opción seleccionada
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
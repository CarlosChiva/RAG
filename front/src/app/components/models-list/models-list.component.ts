import { Component, EventEmitter, Output } from '@angular/core';
import { ModelsService } from '../../services/models.service';
import { CommonModule} from '@angular/common';
import { FormsModule } from '@angular/forms';
import {ModelItem} from '../../interfaces/models.inferface';

@Component({
  selector: 'app-models-list',
  imports: [CommonModule, FormsModule],
  templateUrl: './models-list.component.html',
  styleUrl: './models-list.component.scss'
})
export class ModelsListComponent {
  @Output() modelSelected = new EventEmitter<ModelItem>();

  models: ModelItem[] = [];
  selectedValue: ModelItem = {
    name: '',
    size: ''
  };
  selectedModelName: string = ''; // Nueva propiedad para el ngModel

  constructor(private ModelsService: ModelsService) {}

  ngOnInit(): void {
    this.loadModels();
  }

  loadModels(): void {
    this.ModelsService.getOllamaModels().subscribe({
      next: (data) => {
        console.log('Models from API:', data);
        this.models = data;
        console.log('Models assigned:', this.models);
      },
      error: (error: any) => console.error('Error fetching models:', error)
    });
  }

  // Método para manejar la selección en el dropdown
  onSelectChange(event: any): void {
    const selectedModelName = event.target.value;
    console.log('Selected model name from dropdown:', selectedModelName);

    // Encontrar el modelo completo basado en el nombre seleccionado
    const selectedModel = this.models.find(model => model.name === selectedModelName);
    console.log('Found model object:', selectedModel);
    
    if (selectedModel) {
      this.selectModel(selectedModel);
    } else {
      console.error('No se encontró el modelo con nombre:', selectedModelName);
    }
  }

  selectModel(model: ModelItem): void {
    this.selectedValue = model;
    this.selectedModelName = model.name; // Actualizar el valor para ngModel
    console.log('Selected model in selectModel():', this.selectedValue);
    // Emitir el evento al componente padre
    this.modelSelected.emit(this.selectedValue);
  }
}
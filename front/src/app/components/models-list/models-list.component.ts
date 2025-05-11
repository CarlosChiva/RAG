import { Component } from '@angular/core';
import { ModelsService } from '../../services/models.service';
import { CommonModule} from '@angular/common';
import { FormsModule } from '@angular/forms';
import {ModelItem} from '../../interfaces/models.inferface'; // Definir la interfaz para el mensaje de conversación


@Component({
  selector: 'app-models-list',
  imports: [CommonModule,FormsModule],
  templateUrl: './models-list.component.html',
  styleUrl: './models-list.component.scss'
})
export class ModelsListComponent {
  constructor(
      private ModelsService: ModelsService,

){};
  models: ModelItem[] = [];
  selectedValue: ModelItem ={
    name: '',
    size: ''
  };
  ngOnInit(): void {
    this.loadModels();
  }
  loadModels(): void {
    this.ModelsService.getOllamaModels().subscribe({
      next: (data) => {
        console.log(data);

        this.models=data;
        console.log(this.models);
              },
      error: (error: any) => console.error('Error fetching collections:', error)
    });
  }
  onSelectChange(event:any){
    this.selectedValue = event.target.value
  }
}

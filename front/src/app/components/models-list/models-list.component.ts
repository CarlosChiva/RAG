import { Component } from '@angular/core';
import { ModelsService } from '../../services/models.service';
import { CommonModule} from '@angular/common';
import { FormsModule } from '@angular/forms';


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
  models: string[] = [];
  selectedValue: string = '';
  loadModels(): void {
    this.ModelsService.getOllamaModels().subscribe({
      next: (data) => {
        this.models = data;
              },
      error: (error: any) => console.error('Error fetching collections:', error)
    });
  }
  onSelectChange(event:any){
    this.selectedValue = event.target.value
  }
}

import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-tabla',
  templateUrl: './tabla.component.html',
  styleUrls: ['./tabla.component.scss'],
  standalone: true,
  imports: [CommonModule]
})
export class TablaComponent {
  @Input() data: any = {};

  get columnas(): string[] {
    if (!this.data || Object.keys(this.data).length === 0) return [];
    return Object.keys(this.data);
  }

  get filas(): any[] {
    if (!this.data || Object.keys(this.data).length === 0) return [];
    
    // Determinar cuántas filas hay examinando la primera columna
    const firstColumnKey = this.columnas[0];
    const firstColumn = this.data[firstColumnKey];
    const rowCount = Object.keys(firstColumn).length;
    
    // Crear un array de filas, donde cada fila es un objeto con valores para cada columna
    const rows = [];
    for (let i = 0; i < rowCount; i++) {
      const row: any = {};
      this.columnas.forEach(column => {
        row[column] = this.data[column][i.toString()];
      });
      rows.push(row);
    }
    
    return rows;
  }
}
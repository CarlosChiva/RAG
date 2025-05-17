// src/app/services/collections.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import {ModelItem} from '../interfaces/models.inferface'; // Definir la interfaz para el mensaje de conversación
import {Config} from '../interfaces/config.interface';
// Definir la interfaz para el mensaje de conversación

@Injectable({
  providedIn: 'root'
})
export class ModelsService {
  private apiUrl = 'http://localhost:8003';
  constructor(private http: HttpClient) { }
  // Nueva función para hacer una query
  query(config: Config): Observable<any> {
    const headerss = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`,
        'Content-Type': 'application/json'  // Asegura el tipo de contenido

    });
    
    return this.http.post<string>(`${this.apiUrl}/query`,config, {
        headers: headerss,
        responseType: 'json' as any
}
    );
  }

  // Nueva función para obtener los modelos de Ollama
  getOllamaModels(): Observable<ModelItem[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`
    });
    
    return this.http.get<ModelItem[]>(`${this.apiUrl}/get_ollama_models`, { 
      headers 
    });
  }


}

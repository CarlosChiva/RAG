// src/app/services/collections.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import {ConversationMessage} from '../interfaces/conversations.interface'; // Definir la interfaz para el mensaje de conversación
// Definir la interfaz para el mensaje de conversación

@Injectable({
  providedIn: 'root'
})
export class ModelsService {
  private apiUrl = 'http://localhost:8003';
  constructor(private http: HttpClient) { }
  // Nueva función para hacer una query
  query(query: string, config: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`
    });
    
    return this.http.post(`${this.apiUrl}/query`, { 
      query,
      config 
    }, { observe: 'response' });
  }

  // Nueva función para obtener los modelos de Ollama
  getOllamaModels(): Observable<string[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`
    });
    
    return this.http.get<string[]>(`${this.apiUrl}/get_ollama_models`, { 
      headers 
    });
  }


}

// src/app/services/collections.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

// Definir la interfaz para el mensaje de conversación
export interface ConversationMessage {
  user?: string;
  bot?: string;
}

@Injectable({
  providedIn: 'root'
})
export class CollectionsService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    });
  }

  getCollections(): Observable<{collections_name: string[]}> {
    return this.http.get<{collections_name: string[]}>(`${this.apiUrl}/collections`, {
      headers: this.getHeaders()
    });
  }

  getConversation(collectionName: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/get-conversation`, {
      headers: this.getHeaders(),
      params: { collection_name: collectionName }
    });
  }

  deleteCollection(collectionName: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/delete-collection`, 
      { collection_name: collectionName },
      { headers: this.getHeaders() }
    );
  }

  sendMessage(message: string, collectionName: string): Observable<string> {
    const params = new URLSearchParams({
      input: message,
      collection_name: collectionName
    });
    
    return this.http.get<string>(`${this.apiUrl}/llm-response?${params.toString()}`, {
      headers: this.getHeaders(),
      responseType: 'json' as any
    });
  }
  uploadFiles(files: FileList, collectionName: string): Observable<any> {
    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    
    formData.append('name_collection', collectionName);
    
    return this.http.post(`${this.apiUrl}/add_document`, formData, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      })
    });
  }
}
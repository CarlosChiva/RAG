// src/app/services/collections.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import {ModelItem} from '../interfaces/models.inferface'; // Definir la interfaz para el mensaje de conversación
import {Config} from '../interfaces/config.interface';
// Definir la interfaz para el mensaje de conversación

@Injectable({
  providedIn: 'root'
})
export class ModelsService {
  private apiUrl = 'http://localhost:8003';
  private apiUrlWs = 'ws://localhost:8003';
  // <‑‑ NEW: we keep a reference to the current socket
  private currentWs?: WebSocket;
  // <‑‑ NEW: subject that components can subscribe to in order to be notified when the socket closes
  private socketClosed$ = new Subject<void>();

  constructor(private http: HttpClient) { }
  getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
  }
  // Nueva función para hacer una query
  query(config: Config): Observable<any> {
    const wsUrl = `${this.apiUrlWs}/query`;
  var configuration = {
      credentials: this.getHeaders().get('Authorization'),
      userInput: config.userInput,
      conversation: config.conversation,
      modelName: config.modelName,
      tools: config.tools,
    };
    // guardamos la referencia para cerrar manualmente si fuera necesario
    this.currentWs = new WebSocket(wsUrl);
    return new Observable((observer) => {
      if (!this.currentWs) {
        observer.error('WebSocket not available');
        return;
      }
      // ---------- onopen ----------
      this.currentWs.onopen = () => {
       
        this.currentWs!.send(JSON.stringify(configuration));
      };

      // ---------- onmessage ----------
      this.currentWs.onmessage = (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data);

          /* ---- 1. Mensaje de “fin” ---- */
          if (data.end && data.end === '__END__') {
            observer.complete();          // Completa el observable
            this.currentWs!.close();       // Cierra la conexión
            return;
          }

          /* ---- 2. Mensaje de respuesta regular ---- */
          observer.next(data);           // Envío al suscriptor
        } catch (e) {
          // Si no era JSON (por ejemplo un error de texto plano)
          observer.next(event.data);
        }
      };

      // ---------- onerror ----------
      this.currentWs.onerror = (err) => {
        console.error('WebSocket error:', err);
        observer.error(err);
      };

      // ---------- onclose ----------
      this.currentWs.onclose = () => {
        console.log('WebSocket closed');
        observer.complete();
      };

      // ---------- cleanup ----------
      return () => {
        if (
          this.currentWs &&
          (this.currentWs.readyState === WebSocket.OPEN ||
            this.currentWs.readyState === WebSocket.CONNECTING)
        ) {
          console.log('Closing WebSocket due to unsubscription.');
          this.currentWs.close();
        }
      };
    });
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

  getChats(): Observable<{chats: string[]}> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`
    });
    
    return this.http.get<{chats: string[]}>(`${this.apiUrl}/get_chats`, { 
      headers 
    });
  }
   
  removeChat(collectionName: string): Observable<any> {
    const options = {
      headers: this.getHeaders()
    };
    
    return this.http.post(`${this.apiUrl}/remove-chat`, { chatName: collectionName }, options);
  }
 createChat(newChatName:string): Observable<any> {
  const options = {
    headers: this.getHeaders()
  };

  return this.http.post(`${this.apiUrl}/new_chat`, { chatName: newChatName }, options);
}
 getConversation(chatNAme: string): Observable<any> {
    
  return this.http.get<any>(`${this.apiUrl}/get-conversation`, {
      headers: this.getHeaders(),
      params: { chatName: chatNAme }
    });
  }
  updateChatName(oldChatName: string, newChatName: string): Observable<any> {
    const options = {
      headers: this.getHeaders()
    };
    return this.http.post(`${this.apiUrl}/update-chat-name`, { oldChatName, newChatName }, options);
  }
  
  getToolsConf():Observable<Object>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`
    });
    
    return this.http.get<Object>(`${this.apiUrl}/get_tools_conf`, { 
      headers 
    });
  }
  updateToolsConf(conf:Object):Observable<Object>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${window.localStorage.getItem('token')}`,
      'Content-Type': 'application/json', 
    });
    console.log(`config send ${conf}`);
    
    return this.http.post<Object>(`${this.apiUrl}/update_tools_conf`, conf, { 
      headers 
    });
  }
}

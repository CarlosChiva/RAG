import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {DbConfig} from '../interfaces/db-conf.interface';
@Injectable({
    providedIn: 'root'
  })
  export class DdbbServices {
    private apiUrl = 'http://localhost:8002';
    private apiUrlWs = 'ws://localhost:8002';
  
    constructor(private http: HttpClient) { }
    private getHeaders(): HttpHeaders {
        return new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        });
      }
    getConfigs(): Observable<DbConfig[]> { // mirar los tipos de datos
        return this.http.get<DbConfig[]>(`${this.apiUrl}/get-list-configurations`, {
          headers: this.getHeaders()
        });
      }
    question(message: string, collection: DbConfig): Observable<string> {
        
      const token= this.getHeaders();
      const wsUrl=`${this.apiUrlWs}/question`
      return new Observable(observer => {
        try {
          // Crear conexión WebSocket
          const ws = new WebSocket(wsUrl);
          
          ws.onopen = () => {
            console.log('WebSocket connected');
            
            // Enviar el token como parte del mensaje inicial
            const initialMessage = {
              question: message,
              config: collection,
              auth: this.getHeaders().get('Authorization') // Devuelve: "Bearer token_value"
            };
            
            ws.send(JSON.stringify(initialMessage));
          };
          ws.onmessage = (event) => {
            // Recibir cada token por separado y emitirlo
            observer.next(event as any);
          };
          
          ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            observer.error(error);
          };
          
          ws.onclose = () => {
            console.log('WebSocket closed');
            observer.complete();
          };
          
        } catch (error) {
          observer.error(error);
        }
      });
    };

      
    addConfig(config: DbConfig): Observable<{configs: DbConfig}> {
      return this.http.post<{ configs: DbConfig }>(`${this.apiUrl}/add_configuration`, config, {
        headers: this.getHeaders()
      });
      }
    removeConfig(config: DbConfig): Observable<DbConfig> {
        return this.http.delete<DbConfig>(`${this.apiUrl}/remove-configuration`, {
          headers: this.getHeaders(),
          body: config
        });
      }
    tryConnection(config: DbConfig): Observable<boolean> {
      const params = new HttpParams()
      .set('connection_name', config.connection_name)
      .set('type_db', config.type_db)
      .set('user', config.user)
      .set('password', config.password)
      .set('host', config.host)
      .set('port', config.port)
      .set('database_name', config.database_name);
  
        return this.http.get<boolean>(`${this.apiUrl}/try-connection`, {
          headers: this.getHeaders(),
          params:params
        });
      }

}  
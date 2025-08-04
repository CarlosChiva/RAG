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

    // El tipo de retorno ahora puede ser 'any' porque vamos a devolver
    // objetos parseados, no siempre strings.
    question(message: string, collection: DbConfig): Observable<any> { // <<< CAMBIO 1: Observable<any>
        
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
              auth: this.getHeaders().get('Authorization')
            };
            
            ws.send(JSON.stringify(initialMessage));
          };

          ws.onmessage = (event: MessageEvent) => { // <<< CAMBIO 2: Añadir tipo MessageEvent
            
            // --- INICIO DE LA MODIFICACIÓN CLAVE ---
            try {
              // Extraemos el string del evento
              const jsonDataString = event.data;
              
              // Parseamos el string a un objeto JavaScript
              const parsedData = JSON.parse(jsonDataString);

              // Emitimos el objeto ya parseado al componente suscriptor
              observer.next(parsedData); 
              
            } catch (error) {
              // Si el mensaje no es JSON (ej. un string de control como '__END__'),
              // lo emitimos tal cual.
              observer.next(event.data);
            }
            // --- FIN DE LA MODIFICACIÓN CLAVE ---
          };
          
          ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            observer.error(error);
          };
          
          ws.onclose = () => {
            console.log('WebSocket closed');
            observer.complete();
          };
          
          // <<< CAMBIO 3: Añadir una función de limpieza para cerrar el socket
          // Esta función se ejecutará cuando el componente se desuscriba.
          return () => {
            if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
                console.log('Closing WebSocket due to unsubscription.');
                ws.close();
            }
          };

        } catch (error) {
          observer.error(error);
          // Ensure a value is always returned
          return;
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
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { DbConfig } from '../interfaces/db-conf.interface';

@Injectable({
  providedIn: 'root',
})
export class DdbbServices {
  private apiUrl = 'http://localhost:8002';
  private apiUrlWs = 'ws://localhost:8002';

  // <‑‑ NEW: we keep a reference to the current socket
  private currentWs?: WebSocket;
  // <‑‑ NEW: subject that components can subscribe to in order to be notified when the socket closes
  private socketClosed$ = new Subject<void>();

  constructor(private http: HttpClient) {}

  /* ---------- Helpers ---------- */
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
  }

  /* ---------- API ---------- */
  getConfigs(): Observable<DbConfig[]> {
    return this.http.get<DbConfig[]>(`${this.apiUrl}/get-list-configurations`, {
      headers: this.getHeaders(),
    });
  }

  /* ---------- WebSocket ---------- */
  /**
   * Abre una conexión WebSocket y devuelve un Observable con los datos que llegan.
   * Cuando el servidor envíe el mensaje de cierre (ej.: "__END__") la conexión se cierra automáticamente.
   */
// ddbb.services.ts
  question(message: string, collection: DbConfig): Observable<any> {
    const wsUrl = `${this.apiUrlWs}/question`;

    // guardamos la referencia para cerrar manualmente si fuera necesario
    this.currentWs = new WebSocket(wsUrl);

    return new Observable((observer) => {
      if (!this.currentWs) {
        observer.error('WebSocket not available');
        return;
      }

      // ---------- onopen ----------
      this.currentWs.onopen = () => {
        console.log('WebSocket connected');
        const initMsg = {
          question: message,
          config: collection,
          auth: this.getHeaders().get('Authorization')
        };
        this.currentWs!.send(JSON.stringify(initMsg));
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

  /* ---------- Otros endpoints ---------- */
  addConfig(config: DbConfig): Observable<{ configs: DbConfig }> {
    return this.http.post<{ configs: DbConfig }>(
      `${this.apiUrl}/add_configuration`,
      config,
      {
        headers: this.getHeaders(),
      }
    );
  }

  removeConfig(config: DbConfig): Observable<DbConfig> {
    return this.http.delete<DbConfig>(`${this.apiUrl}/remove-configuration`, {
      headers: this.getHeaders(),
      body: config,
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
      params,
    });
  }

  /* ---------- Notificaciones opcionales ---------- */
  /**
   * Devuelve un Observable que emite cada vez que la conexión WebSocket
   * se cierra (ya sea automáticamente o manualmente).
   */
  onSocketClosed$(): Observable<void> {
    return this.socketClosed$.asObservable();
  }
}
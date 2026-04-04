import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MultimediaService {
  private apiUrl = 'http://localhost:8006';
  private apiUrlWs = 'ws://localhost:8006';
  private currentWs?: WebSocket;
  private socketClosed$ = new Subject<void>();

  constructor(private http: HttpClient) {}

  /** Build the common Authorization header */
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
  }

  /** GET /api/conversations - returns list of conversations */
  listConversations(): Observable<any> {
    return this.http.get(`${this.apiUrl}/api/conversations`, { headers: this.getHeaders() });
  }

  /** POST /api/upload - upload video with multipart/form-data */
  uploadVideo(file: File, metadata?: string): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    if (metadata) {
      formData.append('metadata', metadata);
    }
    // For multipart/form-data, we should not set Content-Type header
    // The browser will set it with the correct boundary
    return this.http.post(`${this.apiUrl}/api/upload`, formData, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      })
    });
  }

  /** GET /api/media/{file_id} - returns video URL */
  getVideo(fileId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/api/media/${fileId}`, { headers: this.getHeaders() });
  }

  /** DELETE /api/media/{file_id} */
  deleteVideo(fileId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/api/media/${fileId}`, { headers: this.getHeaders() });
  }

  /** GET /api/conversations/{id} */
  getConversation(conversationId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/api/conversations/${conversationId}`, { headers: this.getHeaders() });
  }

  /** POST /api/conversations - create a new conversation */
  createConversation(name: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/conversations`, { name }, { headers: this.getHeaders() });
  }

  /** DELETE /api/conversations/{id} - delete a conversation */
  deleteConversation(conversationId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/api/conversations/${conversationId}`, { headers: this.getHeaders() });
  }

  /**
   * Sends a message via the WebSocket with streaming.
   * Uses __END__ marker to detect end of transmission.
   */
  sendMessage(conversationId: string, message: string, onMessage: (data: any) => void): Observable<any> {
    const wsUrl = `${this.apiUrlWs}/api/chat`;

    this.currentWs = new WebSocket(wsUrl);

    return new Observable((observer) => {
      if (!this.currentWs) {
        observer.error('WebSocket not available');
        return;
      }

      this.currentWs.onopen = () => {
        console.log('WebSocket connected (Multimedia service)');
        const initMsg = {
          conversation_id: conversationId,
          message: message,
          auth: this.getHeaders().get('Authorization')
        };
        this.currentWs!.send(JSON.stringify(initMsg));
      };

      this.currentWs.onmessage = (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data);

          /* ---- 1. Mensaje de "fin" ---- */
          if (data.end && data.end === '__END__') {
            observer.complete();
            this.currentWs!.close();
            return;
          }

          /* ---- 2. Mensaje de respuesta regular ---- */
          onMessage(data);
          observer.next(data);
        } catch (e) {
          // Si no era JSON (por ejemplo un error de texto plano)
          onMessage(event.data);
          observer.next(event.data);
        }
      };

      this.currentWs.onerror = (err) => {
        console.error('WebSocket error (Multimedia service)', err);
        observer.error(err);
      };

      this.currentWs.onclose = () => {
        console.log('WebSocket closed (Multimedia service)');
        observer.complete();
        this.socketClosed$.next();
      };

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

  /**
   * Returns an Observable that emits every time the WebSocket connection
   * closes (either automatically or manually).
   */
  onSocketClosed$(): Observable<void> {
    return this.socketClosed$.asObservable();
  }
}

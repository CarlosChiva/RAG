import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExcelService {
  private apiUrl = 'http://localhost:8004';          // REST API base
  private apiUrlWs = 'ws://localhost:8004';          // WebSocket base

  constructor(private http: HttpClient) {}

  /** Build the common Authorization header */
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
  }

  /* ---------- REST endpoints (mirroring rag_excels routes) ---------- */

  /** GET /list_files */
  listFiles(): Observable<any> {
    return this.http.get(`${this.apiUrl}/list_files`, { headers: this.getHeaders() });
  }

  /** GET /get_file  (requires name_file query param) */
  getFile(name_file: string): Observable<any> {
    const params = new HttpParams().set('name_file', name_file);
    return this.http.get(`${this.apiUrl}/get_file`, { headers: this.getHeaders(), params });
  }

  /** POST /upload_file  (multipart/form-data) */
  uploadFile(file: any): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/upload_file`, formData, { headers: this.getHeaders() });
  }

  /** POST /upload_file_edited (multipart/form-data) */
  uploadEditedFile(file: any): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/upload_file_edited`, formData, { headers: this.getHeaders() });
  }

  /** GET /configs */
  getConfigs(): Observable<any> {
    return this.http.get(`${this.apiUrl}/configs`, { headers: this.getHeaders() });
  }

  /* ---------- WebSocket endpoint (mirroring /llm-query) ---------- */

  /**
   * Sends a message via the LLM query WebSocket.
   * Mirrors `CollectionsService.sendMessage` but uses our own ws URL and
   * passes parameters required by the rag_excels `/llm-query` route.
   */
  sendMessage(message: string, collectionName?: string): Observable<string> {
    const wsUrl = `${this.apiUrlWs}/llm-query`;
    return new Observable(observer => {
      try {
        const ws = new WebSocket(`${wsUrl}?${this._buildWsParams(message, collectionName)}`);

        ws.onopen = () => {
          console.log('WebSocket connected (Excel service)');
          // Forward auth header payload if needed
          const initMsg = JSON.stringify({
            input: message,
            collection_name: collectionName,
            auth: this.getHeaders().get('Authorization')
          });
          ws.send(initMsg);
        };

        ws.onmessage = ev => observer.next(ev.data as string);

        ws.onerror = err => {
          console.error('WebSocket error (Excel service)', err);
          observer.error(err);
        };

        ws.onclose = () => observer.complete();

      } catch (err) {
        observer.error(err);
      }
    });
  }

  /** Helper to encode WS query parameters */
  private _buildWsParams(message: string, collectionName?: string): string {
    const params = new URLSearchParams();
    params.set('input', message);
    if (collectionName) {
      params.set('collection_name', collectionName);
    }
    return params.toString();
  }

  /* ---------- Optional cleanup notification ---------- */
  private socketClosed$ = new Subject<void>();
  public onSocketClosed$(): Observable<void> {
    return this.socketClosed$.asObservable();
  }
}

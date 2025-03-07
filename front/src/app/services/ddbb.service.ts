import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
    providedIn: 'root'
  })
  export class DdbbServices {
    private apiUrl = 'http://localhost:8002';
  
    constructor(private http: HttpClient) { }
    private getHeaders(): HttpHeaders {
        return new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        });
      }
    getConfigs(): Observable<{configs: string[]}> { // mirar los tipos de datos
        return this.http.get<{configs: string[]}>(`${this.apiUrl}/get-list-configurations`, {
          headers: this.getHeaders()
        });
      }
    question(): Observable<{configs: string[]}> {
        return this.http.get<{configs: string[]}>(`${this.apiUrl}/question`, {
          headers: this.getHeaders()
        });
      }
    addConfig(config: string): Observable<{configs: string[]}> {
        return this.http.post<{configs: string[]}>(`${this.apiUrl}/add_configuration`, {config}, {
          headers: this.getHeaders()
        });
      }
    removeConfig(config: string): Observable<{configs: string[]}> {
        return this.http.delete<{configs: string[]}>(`${this.apiUrl}/remove-configuration`, {
          headers: this.getHeaders(),
          body: {config}
        });
      }
    tryConnection(config: string): Observable<{configs: string[]}> {
        return this.http.get<{configs: string[]}>(`${this.apiUrl}/try-connection`, {
          headers: this.getHeaders()
        });
      }

}  
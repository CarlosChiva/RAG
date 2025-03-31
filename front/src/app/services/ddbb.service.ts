import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {DbConfig} from '../interfaces/db-conf.interface';
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
    getConfigs(): Observable<DbConfig[]> { // mirar los tipos de datos
        return this.http.get<DbConfig[]>(`${this.apiUrl}/get-list-configurations`, {
          headers: this.getHeaders()
        });
      }
    question(message: string, collection: DbConfig): Observable<string> {
        const params = new HttpParams().set('input', message);
      
        return this.http.post<string>(`${this.apiUrl}/question`, collection, { params });
      }
    addConfig(config: DbConfig): Observable<{configs: DbConfig}> {
      return this.http.post<{ configs: DbConfig }>(`${this.apiUrl}/add_configuration`, config, {
        headers: this.getHeaders()
      });
      }
    removeConfig(config: string): Observable<{configs: string[]}> {
        return this.http.delete<{configs: string[]}>(`${this.apiUrl}/remove-configuration`, {
          headers: this.getHeaders(),
          body: {config}
        });
      }
    tryConnection(config: DbConfig): Observable<boolean> {
      const params = new HttpParams()
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
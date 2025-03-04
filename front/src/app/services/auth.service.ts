// auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

interface AuthResponse {
  access_token: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl_user_ddbb = 'http://localhost:8001';

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<AuthResponse> {
    let params = new HttpParams()
      .set('username', username)
      .set('password', password);
  
    return this.http.get<AuthResponse>(`${this.apiUrl_user_ddbb}/log-in`, { params })
      .pipe(
        tap(response => {
          // Guarda SOLO el token sin el "Bearer "
          localStorage.setItem('access_token', response.access_token);
          localStorage.setItem('user_name', username);
        })
      );
  }
  
  signup(username: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl_user_ddbb}/sing_up`, { username, password })
      .pipe(
        tap(response => {
          // Guarda SOLO el token sin el "Bearer "
          localStorage.setItem('access_token', response.access_token);
          localStorage.setItem('user_name', username);
        })
      );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_name');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  getToken(): string | null {
    const token = localStorage.getItem('access_token');
    return token ? `Bearer ${token}` : null;
  }
}
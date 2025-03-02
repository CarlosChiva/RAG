// menu.component.ts
import { Component, OnInit } from '@angular/core';
import { Router ,RouterLink} from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, HttpClientModule,RouterLink],
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {
  username: string = '';
  sidebarActive: boolean = false;
  
 // Usa rutas relativas a la carpeta assets
 icons: {[key: string]: string} = {
  "pdf": "icons/pdf.png",
  "excel": "icons/excel.png",
  "multimedia": "icons/multimedia.png",
  "audio": "icons/chatbot.png",
  "ddbb": "icons/ddbb.png",
  "chat": "icons/chatbot.png"
};
  services: string[] = [];
  availableServices: string[] = [];

  constructor(
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    const token = localStorage.getItem('access_token');
    this.username = localStorage.getItem('user_name') || '';
    
    if (!token) {
      alert('Token expired. Please, sign up again');
      this.router.navigate(['/login']);
    }
    
    this.fetchServices();
    this.fetchAvailableServices();
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_name');
    this.router.navigate(['/login']);
  }

  openSidebar(): void {
    this.sidebarActive = true;
  }

  closeSidebar(): void {
    this.sidebarActive = false;
  }

  async fetchServices(): Promise<void> {
    try {
      const token = localStorage.getItem('access_token');
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      });

      this.http.get<{services: string[]}>('http://localhost:8001/get-services', { headers })
        .subscribe({
          next: (response) => {
            this.services = response.services;
          },
          error: (error) => {
            console.error('Error al obtener servicios:', error);
          }
        });
    } catch (error) {
      console.error('Error al obtener servicios activos:', error);
    }
  }

  async fetchAvailableServices(): Promise<void> {
    try {
      const token = localStorage.getItem('access_token');
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      });

      this.http.get<{services: string[]}>('http://localhost:8001/get-services-available', { headers })
        .subscribe({
          next: (response) => {
            this.availableServices = response.services;
          },
          error: (error) => {
            console.error('Error al obtener servicios disponibles:', error);
          }
        });
    } catch (error) {
      console.error('Error al obtener servicios disponibles:', error);
    }
  }

  async selectService(service: string): Promise<void> {
    try {
      const token = localStorage.getItem('access_token');
      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      });

      this.http.get(`http://localhost:8001/add-services?service=${encodeURIComponent(service)}`, { headers })
        .subscribe({
          next: () => {
            this.router.navigate([`/${service}`]);
          },
          error: (error) => {
            console.error('Error al añadir servicio:', error);
          }
        });
    } catch (error) {
      console.error('Error al obtener servicios disponibles:', error);
    }
  }
}
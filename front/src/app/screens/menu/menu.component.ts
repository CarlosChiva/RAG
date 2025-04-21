// menu.component.ts
import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { AuthService } from '../../services/auth.service'; // Ajusta la ruta según tu estructura

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterLink],
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
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    if (!this.authService.isAuthenticated()) {
      alert('Token expired. Please, sign up again');
      this.router.navigate(['/login']);
      return;
    }
    
    this.username = this.authService.getUsername();
    this.fetchServices();
    this.fetchAvailableServices();
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  openSidebar(): void {
    this.sidebarActive = true;
  }

  closeSidebar(): void {
    this.sidebarActive = false;
  }

  fetchServices(): void {
    this.authService.getServices().subscribe({
      next: (response) => {
        this.services = response.services;
      },
      error: (error) => {
        console.error('Error al obtener servicios:', error);
      }
    });
  }

  fetchAvailableServices(): void {
    this.authService.getAvailableServices().subscribe({
      next: (response) => {
        this.availableServices = response.services;
      },
      error: (error) => {
        console.error('Error al obtener servicios disponibles:', error);
      }
    });
  }

  selectService(service: string): void {
    this.authService.selectService(service).subscribe({
      next: () => {
        console.log('Servicio seleccionado:', service);
        this.router.navigate([`/${service}`]);
      },
      error: (error) => {
        console.error('Error al añadir servicio:', error);
      }
    });
  }
}
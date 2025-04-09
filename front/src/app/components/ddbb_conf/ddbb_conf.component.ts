import { Component, OnInit, ViewChild, ElementRef, Output, Input, EventEmitter } from '@angular/core';
import { Router} from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DdbbServices } from '../../services/ddbb.service';
import {DbConfig} from '../../interfaces/db-conf.interface';

@Component({
  selector: 'app-ddbb-conf',
  imports: [CommonModule, HttpClientModule,  FormsModule],
  templateUrl: './ddbb_conf.component.html',
  styleUrl: './ddbb_conf.component.scss'
})

export class DdbbConfComponent {
  @Input() dbConfig!: DbConfig;  // Recibe la configuración desde el padre

  @Output() cerrarModal = new EventEmitter<void>(); // Evento para cerrar el modal
  isLoading: boolean = false; // Estado del loader
  
  configList: DbConfig[] = [];
  constructor(
    private router: Router,
    private ddbbServices: DdbbServices
//    private collectionsService: CollectionsService
  ) {}
  ngOnInit(): void {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      alert('Token expired. Please, sign up again');
      this.router.navigate(['/login']);
      return;
    }
    
  }



  cerrar() {
    this.cerrarModal.emit(); // Notifica al componente padre que cierre la ventana emergente
  }
  try_connection(){
    this.isLoading = true; // Activar el loader

    this.ddbbServices.tryConnection(this.dbConfig).subscribe({
      next: (response: boolean) => {
      if (response) {
        console.log("Conexión exitosa");
        alert("Conexión exitosa");
      } else {
        console.log("Conexión fallida");
        alert("No se pudo conectar a la base de datos.");
        this.isLoading = false; // Desactivar el loader cuando la conexión termine

      }
    },
    error: (error) => {
      const backendError = error?.error?.detail;

      console.error("Error de conexión:", error);
      alert(`❌ Error: ${backendError}`);
      this.isLoading = false; // Desactivar el loader cuando la conexión termine

    },
    complete: () => {
      this.isLoading = false; // Desactivar el loader cuando la conexión termine
    }
  });
  };
  save_config(){
    console.log("Enviando configuración:", this.dbConfig);
    
    this.ddbbServices.addConfig(this.dbConfig).subscribe({
      next: (response) => {
        console.log("Configuración guardada con éxito:", response);
        alert("Configuración guardada correctamente.");
      },
      error: (error) => {
        console.error("Error al guardar configuración:", error);
        alert("Hubo un error al guardar la configuración.");
      }
  });
}
}

import { Component, OnInit, ViewChild, ElementRef, Output, Input, EventEmitter } from '@angular/core';
import { Router} from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DdbbServices } from '../../services/ddbb.service';
import {DbConfig} from '../../interfaces/db-conf.interface';

@Component({
  selector: 'app-ddbb-conf',
  imports: [CommonModule,   FormsModule],
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

  isValidConfig(): boolean {
    // Verificar que port sea una cadena de 4 dígitos
    const hasPort = typeof this.dbConfig.port === 'string' && 
                    this.dbConfig.port.length === 4 &&
                    /^\d{4}$/.test(this.dbConfig.port);
    
    // Verificar que host tenga formato de IP (IPv4)
    const isHostValid = /^(?:\d{1,3}\.){3}\d{1,3}$/.test(this.dbConfig.host);

    return hasPort && isHostValid;
  }

  cerrar() {
    this.cerrarModal.emit(); // Notifica al componente padre que cierre la ventana emergente
  }
  try_connection(){
    this.isLoading = true; // Activar el loader

    if (!this.isValidConfig()) {
      alert("La configuración no es válida. Verifique el puerto y el host.");
      this.isLoading = false; // Desactivar el loader
      return;
    }

    this.ddbbServices.tryConnection(this.dbConfig).subscribe({
      next: (response: boolean) => {
      if (response) {
        console.log("Conexión exitosa");
        alert("Conexión exitosa");
      } else {
        console.log("Conexión fallida");
        alert("No se pudo conectar a la base de datos.");
        this.isLoading = false;
      }
    },
    error: (error) => {
      const backendError = error?.error?.detail;

      console.error("Error de conexión:", error);
      alert(`❌ Error: ${backendError}`);
      this.isLoading = false; // Desactivar el loader cuando la conexión termine

    },
    complete: () => {
      this.isLoading = false; 
    }
  });
  };
  save_config(){
    if (!this.isValidConfig()) {
      alert("La configuración no es válida. Verifique el puerto y el host.");
      this.isLoading = false; 
      return;
    }
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

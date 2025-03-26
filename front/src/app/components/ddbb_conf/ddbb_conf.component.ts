import { Component, OnInit, ViewChild, ElementRef, Output, EventEmitter } from '@angular/core';
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
  @Output() cerrarModal = new EventEmitter<void>(); // Evento para cerrar el modal
  isLoading: boolean = false; // Estado del loader

  // Nueva propiedad para la configuración de la base de datos
  dbConfig: DbConfig = {
    type_db: '',
    user: '',
    password: '',
    host: '',
    port: '',
    database_name: ''
  };

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
    
    this.loadCollections();
  }

  loadCollections(): void {
    // this.collectionsService.getCollections().subscribe({
    //   next: (data) => {
    //     this.collections = data.collections_name;
    //   },
    //   error: (error) => console.error('Error fetching collections:', error)
    // });
  }

  openFileDialog(): void {
  //  this.fileInput.nativeElement.click();
  }

  handleFileInput(event: Event): void {
    // const input = event.target as HTMLInputElement;
    // if (input.files && input.files.length > 0) {
    //   this.files = input.files;
    // }
  }

  navigateBack(): void {
    // this.collectionsService.getCollections().subscribe({
    //   next: (data) => {
    //     if (data.collections_name.length === 0) {
    //       alert('No collections found');
    //       this.router.navigate(['/menu']);
    //     } else {
    //       this.router.navigate(['/pdf']);
    //     }
    //   },
    //   error: (error) => {
    //     console.error('Error fetching collections:', error);
    //   }
    // });
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
      console.error("Error de conexión:", error);
      alert("Hubo un error de conexión.");
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

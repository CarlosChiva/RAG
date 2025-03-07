// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { inject } from '@angular/core';
import { AuthGuard } from './guards/auth.guard';
import { MenuComponent } from './components/menu/menu.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'menu', component: MenuComponent, canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: 'pdf', loadComponent: () => import('./components/rag_pdf/rag_pdf.component').then(m => m.PdfComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: 'upload', loadComponent: () => import('./components/upload_pdf/upload_pdf.component').then(m => m.UploadComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: 'ddbb', loadComponent: () => import('./components/rag-ddbb/rag-ddbb.component').then(m => m.RagDdbbComponent), canActivate: [() => inject(AuthGuard).canActivate()] },

  //   { path: 'chat', loadComponent: () => import('./components/chat/chat.component').then(m => m.ChatComponent), canActivate: [() => inject(AuthGuard).canActivate()] },

//   { path: 'excel', loadComponent: () => import('./components/excel/excel.component').then(m => m.ExcelComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
//   { path: 'multimedia', loadComponent: () => import('./components/multimedia/multimedia.component').then(m => m.MultimediaComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
//   { path: 'audio', loadComponent: () => import('./components/audio/audio.component').then(m => m.AudioComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: '**', redirectTo: '/login' }
];
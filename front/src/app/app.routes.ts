// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { LoginComponent } from './screens/login/login.component';
import { inject } from '@angular/core';
import { AuthGuard } from './guards/auth.guard';
import { MenuComponent } from './screens/menu/menu.component';
import { PdfComponent } from './screens/rag_pdf/rag_pdf.component';
//import { UploadComponent } from './components/upload_pdf/upload_pdf.component';
import { RagDdbbComponent } from './screens/rag_ddbb/rag_ddbb.component';
import { ChatbotComponent } from './screens/chatbot/chatbot.component';
export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'menu', component: MenuComponent, canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: 'pdf', component: PdfComponent, canActivate: [() => inject(AuthGuard).canActivate()] },
  //{ path: 'upload', component:UploadComponent, canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: 'ddbb', component:RagDdbbComponent , canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: 'chatbot', component: ChatbotComponent, canActivate: [() => inject(AuthGuard).canActivate()] },

  //   { path: 'excel', loadComponent: () => import('./components/excel/excel.component').then(m => m.ExcelComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
//   { path: 'multimedia', loadComponent: () => import('./components/multimedia/multimedia.component').then(m => m.MultimediaComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
//   { path: 'audio', loadComponent: () => import('./components/audio/audio.component').then(m => m.AudioComponent), canActivate: [() => inject(AuthGuard).canActivate()] },
  { path: '**', redirectTo: '/login' }
];
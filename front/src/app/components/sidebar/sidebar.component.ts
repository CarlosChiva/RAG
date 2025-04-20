// sidebar.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  @Input() title: string = 'Sidebar';
  @Input() sidebarCollapsed: boolean = false;
  
  @Output() toggleSidebarEvent = new EventEmitter<void>();
  
  // Método para colapsar/expandir el sidebar
  toggleSidebar(): void {

    this.toggleSidebarEvent.emit();
    }  
  }

import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-button-container',
  imports: [],
  templateUrl: './button-container.component.html',
  styleUrl: './button-container.component.scss'
})
export class ButtonContainerComponent {
  constructor(private router: Router){}
  logout(): void {
    if (confirm('Are you sure you want to logout?')) {
      localStorage.removeItem('access_token');
      this.router.navigate(['/login']);
    }
  }
  navigateToMenu(): void {
    this.router.navigate(['/menu']);

  }
}

// src/app/components/login/login.component.ts
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  isSignUpMode = false;
  isToggling = false; // Añadido para resolver el error
  formTitle = 'Log in';
  submitButtonText = 'Log In';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    // Verificar si el usuario ya está autenticado
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/menu']);
    }
  }

  toggleMode(event: Event): void {
    event.preventDefault();
    this.isToggling = true; // Añadimos el inicio de la animación
    this.isSignUpMode = !this.isSignUpMode;

    // Actualizar textos según el modo
    if (this.isSignUpMode) {
      this.formTitle = 'Sign Up';
      this.submitButtonText = 'Sign Up';
    } else {
      this.formTitle = 'Log in';
      this.submitButtonText = 'Log In';
    }
    
    // Desactivamos la clase después de la animación
    setTimeout(() => {
      this.isToggling = false;
    }, 500);
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }
    
    const { username, password } = this.loginForm.value;
    
    if (this.isSignUpMode) {
      this.handleSignUp(username, password);
    } else {
      this.handleLogin(username, password);
    }
  }

  private handleLogin(username: string, password: string): void {
    this.authService.login(username, password).subscribe({
      next: (result) => {
        this.router.navigate(['/menu']);
      },
      error: (error) => {
        console.error(error);
        alert(error.message || 'Login failed');
      }
    });
  }

  private handleSignUp(username: string, password: string): void {
    this.authService.signup(username, password).subscribe({
      next: (result) => {
        this.router.navigate(['/menu']);
      },
      error: (error) => {
        console.error(error);
        alert(error.message || 'Sign-up failed');
      }
    });
  }
}
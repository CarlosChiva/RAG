# Login Screen

## Introduction

Authentication screen providing login and sign-up functionality for the RAG application. Implements reactive forms with validation and mode toggling between login and registration.

## Files Documentation

### login.component.ts

**Purpose:** Manages user authentication with login and sign-up modes.

**Main Components:**
- `LoginComponent`: Standalone component implementing OnInit

**Properties:**
- `loginForm`: Reactive form with username and password fields
- `isSignUpMode`: Mode toggle state
- `isToggling`: Animation state for mode switch
- `formTitle`: Dynamic title text
- `submitButtonText`: Dynamic button text

**Methods:**
- `toggleMode()`: Switches between login and sign-up modes with animation
- `onSubmit()`: Form submission handler
- `handleLogin()`: Login via AuthService with navigation
- `handleSignUp()`: Registration via AuthService

**Dependencies:**
- `@angular/core`: Component, OnInit
- `@angular/router`: Router
- `@angular/forms`: FormBuilder, FormGroup, Validators, ReactiveFormsModule
- `@angular/common`: CommonModule
- `AuthService`: Authentication service

**Integration:**
- Route: `/login`
- Redirects to `/menu` on successful authentication
- Checks existing authentication on init

### login.component.html

**Purpose:** Template for authentication form.

**Structure:**
- Dynamic title based on mode
- Reactive form with username and password fields
- Submit button with dynamic text
- Mode toggle link

### login.component.scss

**Purpose:** Styling for authentication screen.

**Key Styles:**
- Form layout and centering
- Input field styling
- Button styling
- Mode toggle animation

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

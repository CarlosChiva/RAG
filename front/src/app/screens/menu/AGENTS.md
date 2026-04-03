# Menu Screen

## Introduction

Main navigation screen providing access to all RAG services (PDF, Excel, Database, Chatbot, Multimedia, Audio). Displays available and selected services with sidebar navigation for mobile responsiveness.

## Files Documentation

### menu.component.ts

**Purpose:** Manages main menu navigation and service selection.

**Main Components:**
- `MenuComponent`: Standalone component implementing OnInit

**Properties:**
- `username`: Current user name from AuthService
- `sidebarActive`: Mobile sidebar visibility state
- `icons`: Service icon path mapping
- `services`: Array of user-selected services
- `availableServices`: Array of available services

**Methods:**
- `logout()`: Clears authentication and navigates to login
- `openSidebar()`: Opens mobile sidebar
- `closeSidebar()`: Closes mobile sidebar
- `fetchServices()`: Fetches user's selected services
- `fetchAvailableServices()`: Fetches available services
- `selectService()`: Selects service and navigates to route
- `onResize()`: Window resize handler for sidebar

**Dependencies:**
- `@angular/core`: Component, OnInit, HostListener
- `@angular/router`: Router, RouterLink
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `AuthService`: Authentication service

**Integration:**
- Route: `/menu` (protected by AuthGuard)
- Fetches services from AuthService
- Icon mapping for service cards

### menu.component.html

**Purpose:** Template for main menu navigation.

**Structure:**
- Header with user name and menu toggle
- Service cards grid with icons and selection
- Mobile sidebar with navigation links

### menu.component.scss

**Purpose:** Styling for main menu screen.

**Key Styles:**
- Service card grid layout
- Responsive design
- Mobile sidebar styling
- Icon styling

### menu.component.spec.ts

**Purpose:** Unit test suite for menu functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

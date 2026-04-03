# Button Container Component

## Introduction

Container component that provides navigation controls and logout functionality for the RAG application. Serves as a reusable navigation element positioned within sidebar layouts.

## Files Documentation

### button-container.component.ts

**Purpose:** Manages user navigation and session termination.

**Main Components:**
- `ButtonContainerComponent`: Standalone component class
- `logout()`: Session termination method with confirmation dialog
- `navigateToMenu()`: Navigation to main menu screen

**Dependencies:**
- `@angular/core`: Component decorator
- `@angular/router`: Router service and RouterLink

**Integration:**
- Injects `Router` service for navigation
- Clears `access_token` from localStorage on logout
- Used in: `chatbot-interaction`, `rag_pdf`, `rag_ddbb`, `excels` screens

### button-container.component.html

**Purpose:** Template defining button layout and click handlers.

**Structure:**
- Logout button with confirmation
- Menu navigation button

### button-container.component.scss

**Purpose:** Styling for button container layout and visual appearance.

**Key Styles:**
- Button positioning within sidebar
- Hover states and visual feedback

### button-container.component.spec.ts

**Purpose:** Unit test suite for button container functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

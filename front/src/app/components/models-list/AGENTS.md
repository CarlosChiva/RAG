# Models List Component

## Introduction

Dropdown component for selecting Ollama models in the chatbot screen. Fetches available models from the backend and emits selection events to parent components.

## Files Documentation

### models-list.component.ts

**Purpose:** Manages model selection dropdown with backend integration.

**Main Components:**
- `ModelsListComponent`: Standalone component

**Properties:**
- `models`: Array of available ModelItem objects
- `selectedValue`: Currently selected model
- `selectedModelName`: Model name for ngModel binding

**Methods:**
- `loadModels()`: Fetches models from ModelsService
- `onSelectChange()`: Dropdown change handler
- `selectModel()`: Model selection with event emission

**Dependencies:**
- `@angular/core`: Component, Output, EventEmitter
- `@angular/common`: CommonModule
- `@angular/forms`: FormsModule
- `ModelsService`: Service for model API calls
- `ModelItem`: Model interface

**Events:**
- `modelSelected`: Selection event containing ModelItem

**Integration:**
- Used in: `chatbot-interaction`, `chatbot` screen
- Fetches models from Ollama backend
- Emits selected model to parent for query configuration

### models-list.component.html

**Purpose:** Template for model selection dropdown.

**Structure:**
- Select element with ngModel binding
- Option list populated from models array

### models-list.component.scss

**Purpose:** Styling for models list dropdown.

**Key Styles:**
- Dropdown positioning
- Option list styling

### models-list.component.spec.ts

**Purpose:** Unit test suite for models list functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

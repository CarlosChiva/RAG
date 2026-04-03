# Database Configuration Component

## Introduction

Modal component for creating and editing database connection configurations. Provides form validation, connection testing, and configuration persistence for RAG database queries.

## Files Documentation

### ddbb_conf.component.ts

**Purpose:** Manages database configuration form and connection testing.

**Main Components:**
- `DdbbConfComponent`: Standalone component with form handling

**Properties:**
- `dbConfig`: Database configuration object (DbConfig interface)
- `isLoading`: Loader state for async operations
- `configList`: Array of existing configurations

**Methods:**
- `isValidConfig()`: Validates port (4-digit string) and host (IPv4 format)
- `cerrar()`: Closes modal and emits event to parent
- `try_connection()`: Tests database connectivity via WebSocket
- `save_config()`: Persists configuration to backend

**Dependencies:**
- `@angular/core`: Component, OnInit, Input, Output, EventEmitter
- `@angular/router`: Router
- `@angular/common`: CommonModule
- `@angular/forms`: FormsModule
- `DdbbServices`: Database service for API calls
- `DbConfig`: Configuration interface

**Events:**
- `cerrar`: Modal close notification to parent

**Integration:**
- Used in: `rag_ddbb` screen
- Receives configuration via @Input
- Emits close event for modal management

### ddbb_conf.component.html

**Purpose:** Template for database configuration form.

**Structure:**
- Form fields: connection name, database type, user, password, host, port, database name/path
- Connection test button with loader
- Save configuration button
- Close modal button

### ddbb_conf.component.scss

**Purpose:** Styling for database configuration modal.

**Key Styles:**
- Modal layout and positioning
- Form field styling
- Button states and loader animation

### ddbb_conf.component.spec.ts

**Purpose:** Unit test suite for database configuration functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

# Chat Output Component

## Introduction

Generic chat output component used for PDF and database RAG screens. Handles message rendering with optional table data display and auto-scroll functionality.

## Files Documentation

### chat-output.component.ts

**Purpose:** Renders chat messages with optional table data support.

**Main Components:**
- `ChatOutputComponent`: Standalone component implementing AfterViewChecked
- `scrollToBottom()`: Auto-scrolls chat to latest message
- `getChatOutputElement()`: Exposes chat output ElementRef for parent components

**Dependencies:**
- `@angular/core`: Component, Input, ViewChild, ElementRef, AfterViewChecked
- `@angular/common`: CommonModule
- `TablaComponent`: Child component for table rendering

**Inputs:**
- `messages`: Array of chat messages
- `showTables`: Boolean flag for table display

**Integration:**
- Imports `TablaComponent` for table data rendering
- Used in: `rag_pdf`, `rag_ddbb` screens

### chat-output.component.html

**Purpose:** Template for rendering chat messages and table data.

**Structure:**
- Message list container
- Conditional table rendering based on `showTables` flag

### chat-output.component.scss

**Purpose:** Styling for chat output layout and message display.

**Key Styles:**
- Message bubble styling
- Table container layout
- Scroll behavior

### chat-output.component.spec.ts

**Purpose:** Unit test suite for chat output functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

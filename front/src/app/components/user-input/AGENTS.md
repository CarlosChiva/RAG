# User Input Component

## Introduction

Generic user input component for message entry in RAG screens (PDF, database, Excel). Provides text input with send functionality and keyboard shortcut support.

## Files Documentation

### user-input.component.ts

**Purpose:** Manages user message input with bidirectional binding.

**Main Components:**
- `UserInputComponent`: Standalone component

**Inputs:**
- `placeholder`: Input placeholder text
- `isSending`: Sending state for disable
- `disabled`: Input disabled state
- `sendButtonText`: Send button label
- `message`: Bidirectional message binding (getter/setter)

**Outputs:**
- `messageChange`: Message change event
- `sendMessage`: Send message event

**Properties:**
- `_message`: Internal message buffer

**Methods:**
- `onInputChange()`: Input change handler with event emission
- `onSendMessage()`: Send message handler with validation
- `onKeyDown()`: Keyboard handler (Enter to send)

**Dependencies:**
- `@angular/core`: Component, EventEmitter, Input, Output
- `@angular/common`: CommonModule

**Integration:**
- Used in: `rag_pdf`, `rag_ddbb`, `excels` screens
- Bidirectional binding via getter/setter pattern
- Enter key shortcut for sending

### user-input.component.html

**Purpose:** Template for user input form.

**Structure:**
- Input field with placeholder
- Send button with label

### user-input.component.scss

**Purpose:** Styling for user input form.

**Key Styles:**
- Input field styling
- Button positioning and states
- Disabled state styling

### user-input.component.spec.ts

**Purpose:** Unit test suite for user input functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

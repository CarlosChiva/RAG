# Upload MCP Configuration Component

## Introduction

Modal component for uploading and editing MCP (Model Context Protocol) configurations. Supports both file upload and direct JSON text input with drag-drop functionality. Used for configuring MCP tools in the chatbot.

## Files Documentation

### upload_mcp.component.ts

**Purpose:** Manages MCP configuration upload and editing.

**Main Components:**
- `UploadMCPComponent`: Standalone component

**Properties:**
- `editConfig`: Configuration object for edit mode
- `isLoading`: Upload state
- `file`: Selected file
- `jsonInput`: JSON content buffer
- `useFile`: File upload mode flag
- `showPreview`: Textarea visibility flag

**Methods:**
- `onUseFileChange()`: Toggles file/text input mode
- `openFileDialog()`: Triggers file input click
- `handleFileInput()`: File selection handler
- `onDragOver/onDragLeave/onDrop()`: Drag-drop handlers
- `readFile()`: Reads file content to jsonInput
- `uploadFiles()`: Validates and sends configuration via ModelsService
- `cerrar()`: Closes modal

**Dependencies:**
- `@angular/core`: Component, ViewChild, ElementRef, Output, EventEmitter, Input
- `@angular/router`: Router
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `@angular/forms`: FormsModule
- `ModelsService`: Service for configuration API calls

**Events:**
- `cerrarMCPModal`: Modal close notification

**Integration:**
- Used in: `chatbot-interaction`, `chatbot` screen
- Uploads mcp_tools configuration to backend
- Supports edit mode with pre-loaded configuration

### upload_mcp.component.html

**Purpose:** Template for MCP configuration upload interface.

**Structure:**
- Mode toggle checkbox (file vs text)
- File input with drag-drop zone
- JSON textarea for preview/edit
- Upload button with loader
- Close button

### upload_mcp.component.scss

**Purpose:** Styling for MCP upload modal.

**Key Styles:**
- Modal layout
- Drag-drop zone styling
- Form field styling
- Loader animation

### upload_mcp.component.spec.ts

**Purpose:** Unit test suite for MCP upload functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

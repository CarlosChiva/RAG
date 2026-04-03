# Upload Comfy Configuration Component

## Introduction

Modal component for uploading and editing ComfyUI workflow configurations. Supports both file upload and direct JSON text input with drag-drop functionality. Used for configuring image generation tools in the chatbot.

## Files Documentation

### upload_comfy.component.ts

**Purpose:** Manages ComfyUI configuration upload and editing.

**Main Components:**
- `UploadComfyComponent`: Standalone component implementing OnInit

**Properties:**
- `editConfig`: Configuration object for edit mode
- `positivePromptNode`: Positive prompt node number
- `isLoading`: Upload state
- `file`: Selected file
- `useFile`: File upload mode flag (true=file, false=text)
- `jsonInput`: JSON content buffer
- `showPreview`: Textarea visibility flag
- `isEditMode`: Edit mode state

**Methods:**
- `onUseFileChange()`: Toggles file/text input mode
- `openFileDialog()`: Triggers file input click
- `handleFileInput()`: File selection handler
- `onDragOver/onDragLeave/onDrop()`: Drag-drop handlers
- `readFile()`: Reads file content to jsonInput
- `uploadFiles()`: Validates and sends configuration via ModelsService
- `cerrar()`: Closes modal

**Dependencies:**
- `@angular/core`: Component, OnInit, ViewChild, ElementRef, Output, EventEmitter, Input
- `@angular/router`: Router
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `@angular/forms`: FormsModule
- `ModelsService`: Service for configuration API calls

**Events:**
- `cerrarImageModal`: Modal close notification

**Integration:**
- Used in: `chatbot-interaction`, `chatbot` screen
- Uploads image_tools configuration to backend
- Supports edit mode with pre-loaded configuration

### upload_comfy.component.html

**Purpose:** Template for ComfyUI configuration upload interface.

**Structure:**
- Mode toggle checkbox (file vs text)
- File input with drag-drop zone
- JSON textarea for preview/edit
- Positive prompt node input
- Upload button with loader
- Close button

### upload_comfy.component.scss

**Purpose:** Styling for ComfyUI upload modal.

**Key Styles:**
- Modal layout
- Drag-drop zone styling
- Form field styling
- Loader animation

### upload_comfy.component.spec.ts

**Purpose:** Unit test suite for ComfyUI upload functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

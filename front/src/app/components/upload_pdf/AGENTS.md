# Upload PDF Component

## Introduction

Modal component for uploading PDF documents to RAG collections. Supports collection selection, new collection creation, and multi-file upload with drag-drop functionality.

## Files Documentation

### upload_pdf.component.ts

**Purpose:** Manages PDF document upload to collections.

**Main Components:**
- `UploadComponent`: Standalone component implementing OnInit

**Properties:**
- `collections`: Array of existing collection names
- `selectedCollection`: Selected existing collection
- `newCollection`: New collection name input
- `isLoading`: Upload state
- `files`: Selected files list

**Methods:**
- `loadCollections()`: Fetches collections from CollectionsService
- `openFileDialog()`: Triggers file input click
- `handleFileInput()`: File selection handler
- `navigateBack()`: Navigation handler when no collections exist
- `onDragOver/onDragLeave/onDrop()`: Drag-drop handlers
- `uploadFiles()`: Validates and uploads files via CollectionsService
- `cerrar()`: Closes modal

**Dependencies:**
- `@angular/core`: Component, OnInit, ViewChild, ElementRef, Output, EventEmitter
- `@angular/router`: Router
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `@angular/forms`: FormsModule
- `CollectionsService`: Service for collection API calls

**Events:**
- `cerrarModal`: Modal close notification

**Integration:**
- Used in: `rag_pdf` screen
- Supports both existing and new collections
- Multi-file upload support

### upload_pdf.component.html

**Purpose:** Template for PDF upload interface.

**Structure:**
- Collection selection dropdown
- New collection name input
- File input with drag-drop zone
- Upload button with loader
- Back navigation button
- Close button

### upload_pdf.component.scss

**Purpose:** Styling for PDF upload modal.

**Key Styles:**
- Modal layout
- Drag-drop zone styling
- Form field styling
- Loader animation

### upload_pdf.component.spec.ts

**Purpose:** Unit test suite for PDF upload functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

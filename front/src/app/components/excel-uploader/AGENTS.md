# Excel Uploader Component

## Introduction

Modal component for uploading Excel files (.xlsx) to the RAG system. Supports both file selection and drag-and-drop functionality for file uploads.

## Files Documentation

### excel-uploader.component.ts

**Purpose:** Handles Excel file upload with validation and drag-drop support.

**Main Components:**
- `ExcelUploaderComponent`: Standalone component implementing OnInit

**Properties:**
- `selectedFileName`: Name of selected file
- `isDragOver`: Drag hover state

**Methods:**
- `onSelect()`: File input change handler with validation
- `onDragOver()`: Drag hover event handler
- `onDragLeave()`: Drag leave event handler
- `onDrop()`: File drop handler with validation
- `isValidFile()`: Validates .xlsx extension
- `uploadFile()`: Sends file to ExcelService

**Dependencies:**
- `@angular/core`: Component, OnInit, Output, EventEmitter
- `ExcelService`: Service for file upload API calls

**Events:**
- `cerrarModal`: Modal close notification
- `fileUploaded`: Upload success notification

**Integration:**
- Used in: `excels` screen
- Validates file extension before upload
- Uses FormData for multipart upload

### excel-uploader.component.html

**Purpose:** Template for Excel file upload interface.

**Structure:**
- File input element
- Drag-drop zone with visual feedback
- File name display

### excel-uploader.component.scss

**Purpose:** Styling for Excel uploader modal.

**Key Styles:**
- Drag-drop zone styling
- Hover state visual feedback
- File input styling

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

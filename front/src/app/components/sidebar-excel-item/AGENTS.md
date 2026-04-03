# Sidebar Excel Item Component

## Introduction

List item component for displaying Excel files in the RAG Excel screen sidebar. Provides selection, deletion, and visibility toggle functionality for uploaded Excel files.

## Files Documentation

### sidebar-excel-item.component.ts

**Purpose:** Manages individual Excel file item in sidebar list.

**Main Components:**
- `SidebarExcelItemComponent`: Standalone component

**Inputs:**
- `itemName`: Excel file name
- `isShown`: Visibility state
- `isSelected`: Selection state

**Outputs:**
- `deleteItem`: Deletion event
- `toggleShow`: Visibility toggle event
- `selectItem`: Selection event

**Methods:**
- `onDelete()`: Deletion handler with API call to ExcelService
- `onToggleShow()`: Visibility toggle handler
- `onSelect()`: Selection handler

**Dependencies:**
- `@angular/core`: Component, Input, Output, EventEmitter
- `@angular/common`: CommonModule
- `ExcelService`: Service for Excel file API calls

**Integration:**
- Used in: `excels` screen
- Calls deleteFile API on deletion
- Emits events for parent state management

### sidebar-excel-item.component.html

**Purpose:** Template for Excel file list item.

**Structure:**
- File name display
- Visibility toggle button
- Delete button
- Selection indicator

### sidebar-excel-item.component.scss

**Purpose:** Styling for Excel file list items.

**Key Styles:**
- Selection highlighting
- Hover states
- Button positioning

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

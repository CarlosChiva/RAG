# Sidebar Database Item Component

## Introduction

List item component for displaying database configurations in the RAG database screen sidebar. Provides selection with connection verification, editing, and deletion functionality.

## Files Documentation

### sidebar-ddbb-item.component.ts

**Purpose:** Manages individual database configuration item in sidebar list.

**Main Components:**
- `SidebarItemComponent`: Standalone component

**Inputs:**
- `item`: Database configuration (DbConfig or string)
- `isSelected`: Selection state
- `displayField`: Field name for display value
- `showEditButton`: Edit button visibility flag

**Outputs:**
- `selectItem`: Selection event
- `editItem`: Edit event
- `deleteItem`: Deletion event
- `itemDeleted`: Deletion confirmation
- `connectionError`: Connection error event
- `openModal`: Modal open event with DbConfig

**Methods:**
- `getDisplayValue()`: Returns connection_name for DbConfig or string value
- `onSelect()`: Selection handler with connection verification via tryConnection
- `onDelete()`: Deletion handler with API call
- `onEdit()`: Edit handler that emits DbConfig for modal

**Dependencies:**
- `@angular/core`: Component, Input, Output, EventEmitter
- `@angular/common`: CommonModule
- `DdbbServices`: Service for database API calls
- `DbConfig`: Configuration interface

**Integration:**
- Used in: `rag_ddbb` screen
- Verifies database connectivity before selection
- Emits configuration for edit modal

### sidebar-ddbb-item.component.html

**Purpose:** Template for database configuration list item.

**Structure:**
- Display text (connection name)
- Edit button (conditional)
- Delete button

### sidebar-ddbb-item.component.scss

**Purpose:** Styling for database list items.

**Key Styles:**
- Selection highlighting
- Hover states
- Button positioning

### sidebar-ddbb-item.component.spec.ts

**Purpose:** Unit test suite for database item functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

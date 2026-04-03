# Sidebar PDF Item Component

## Introduction

List item component for displaying PDF collections in the RAG PDF screen sidebar. Provides selection with conversation loading and deletion functionality.

## Files Documentation

### sidebar-pdf-item.component.ts

**Purpose:** Manages individual PDF collection item in sidebar list.

**Main Components:**
- `SidebarItemComponent`: Standalone component

**Inputs:**
- `collection`: Collection name
- `isSelected`: Selection state
- `displayField`: Field name for display value

**Outputs:**
- `selectItem`: Selection event
- `deleteItem`: Deletion event
- `itemDeleted`: Deletion confirmation
- `conversationLoaded`: Conversation data loaded

**Methods:**
- `getDisplayValue()`: Returns collection name
- `onSelect()`: Selection handler with conversation fetch via CollectionsService
- `onDelete()`: Deletion handler with API call

**Dependencies:**
- `@angular/core`: Component, Input, Output, EventEmitter
- `@angular/common`: CommonModule
- `CollectionsService`: Service for collection API calls

**Integration:**
- Used in: `rag_pdf` screen
- Fetches conversation history on selection
- Emits events for parent state management

### sidebar-pdf-item.component.html

**Purpose:** Template for PDF collection list item.

**Structure:**
- Collection name display
- Delete button
- Selection indicator

### sidebar-pdf-item.component.scss

**Purpose:** Styling for PDF collection list items.

**Key Styles:**
- Selection highlighting
- Hover states
- Button positioning

### sidebar-pdf-item.component.spec.ts

**Purpose:** Unit test suite for PDF item functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

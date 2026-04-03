# Sidebar Conversations Item Component

## Introduction

List item component for displaying chat conversations in the chatbot screen sidebar. Provides selection, deletion, and renaming functionality for chat conversations.

## Files Documentation

### sidebar-conversations-item.component.ts

**Purpose:** Manages individual chat conversation item in sidebar list.

**Main Components:**
- `SidebarItemComponent`: Standalone component

**Inputs:**
- `collection`: Chat conversation name
- `isSelected`: Selection state
- `displayField`: Field name for display value

**Outputs:**
- `selectItem`: Selection event
- `deleteItem`: Deletion event
- `itemDeleted`: Deletion confirmation
- `conversationLoaded`: Conversation data loaded

**Properties:**
- `editing`: Edit mode state
- `newCollectionName`: New name buffer for renaming

**Methods:**
- `getDisplayValue()`: Returns display text for item
- `onSelect()`: Selection handler with conversation fetch
- `onDelete()`: Deletion handler with API call
- `toggleEdit()`: Toggles edit mode
- `saveEdit()`: Saves renamed conversation

**Dependencies:**
- `@angular/core`: Component, Input, Output, EventEmitter
- `@angular/common`: CommonModule
- `@angular/forms`: FormsModule
- `ModelsService`: Service for chat API calls

**Integration:**
- Used in: `chatbot-interaction`, `chatbot` screen
- Fetches conversation data on selection
- Handles chat renaming via ModelsService

### sidebar-conversations-item.component.html

**Purpose:** Template for chat conversation list item.

**Structure:**
- Display text with selection highlighting
- Edit button for renaming
- Delete button
- Input field for edit mode

### sidebar-conversations-item.component.scss

**Purpose:** Styling for conversation list items.

**Key Styles:**
- Selection highlighting
- Hover states
- Edit mode styling

### sidebar-conversation-item.component.spec.ts

**Purpose:** Unit test suite for conversation item functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

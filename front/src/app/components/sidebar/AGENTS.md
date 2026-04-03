# Sidebar Component

## Introduction

Generic collapsible sidebar container component used across multiple screens. Provides structural layout for sidebar content with collapse/expand functionality and event emission for parent component synchronization.

## Files Documentation

### sidebar.component.ts

**Purpose:** Manages sidebar container layout and collapse state.

**Main Components:**
- `SidebarComponent`: Standalone component

**Inputs:**
- `title`: Sidebar header text (default: 'Sidebar')
- `sidebarCollapsed`: Collapse state boolean

**Outputs:**
- `toggleSidebarEvent`: Emitted when toggle button is clicked

**Methods:**
- `toggleSidebar()`: Emits toggle event to parent

**Dependencies:**
- `@angular/core`: Component, Input, Output, EventEmitter

**Integration:**
- Used in: `chatbot-interaction`, `rag_pdf`, `rag_ddbb`, `excels` screens
- Parent component manages actual collapse state
- Content projected via ng-content

### sidebar.component.html

**Purpose:** Template for sidebar container structure.

**Structure:**
- Header with title and toggle button
- Content area for projected child components

### sidebar.component.scss

**Purpose:** Styling for sidebar container.

**Key Styles:**
- Sidebar width transitions
- Header styling
- Content area layout

### sidebar.component.spec.ts

**Purpose:** Unit test suite for sidebar functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

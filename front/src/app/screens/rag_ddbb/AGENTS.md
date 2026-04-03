# RAG Database Screen

## Introduction

Screen for RAG with database queries. Provides chat interface for querying configured databases with sidebar navigation, configuration modal, and real-time response streaming including table data via WebSocket.

## Files Documentation

### rag_ddbb.component.ts

**Purpose:** Manages database RAG chat interface with configuration management.

**Main Components:**
- `RagDdbbComponent`: Standalone component implementing OnInit

**Properties:**
- `sidebarCollapsed`: Sidebar collapse state
- `configs/configList`: Array of database configurations
- `conversation`: Conversation history
- `dbConfig`: Current configuration object
- `selectedConfig`: Selected database configuration
- `hasValidConfig`: Configuration validity flag
- `tableData`: Table data for display
- `message/currentMessage`: Message input buffers
- `messages`: Chat message array with text, isUser, isTyping, tableData
- `isSending`: Sending state
- `mostrarModal`: Configuration modal visibility

**Methods:**
- `abrirModal/cerrarModal()`: Modal management with config
- `getEmptyConfig()`: Returns empty DbConfig
- `toggleSidebar()`: Sidebar collapse toggle
- `loadConfigs()`: Fetches configurations from DdbbServices
- `onSelectItem()`: Configuration selection
- `handleConnectionError()`: Connection error handler
- `onItemDeleted()`: Deletion handler with reload
- `onMessageChange()`: Message input change
- `sendMessage()`: Sends query via WebSocket with table support
- `handleKeyPress()`: Enter key handler
- `scrollChatToBottom()`: Auto-scroll

**Dependencies:**
- `@angular/core`: Component, OnInit, ViewChild, ElementRef
- `@angular/router`: Router, RouterLink
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `@angular/forms`: FormsModule
- `@angular/platform-browser`: DomSanitizer, SafeHtml
- `marked`: Markdown parsing
- `DdbbServices`: Database service
- `DbConfig`: Configuration interface
- Child components: DdbbConfComponent, ChatOutputComponent, SidebarComponent, SidebarItemComponent, ButtonContainerComponent, UserInputComponent

**Integration:**
- Route: `/ddbb` (protected by AuthGuard)
- WebSocket streaming via DdbbServices.question
- Handles response, table, and error events
- Opens configuration modal when no configs exist

### rag_ddbb.component.html

**Purpose:** Template for database RAG chat interface.

**Structure:**
- Container with sidebar and main content
- Sidebar with configuration list
- Chat output area with table support
- User input component
- Configuration modal overlay

### rag_ddbb.component.scss

**Purpose:** Styling for database RAG screen.

**Key Styles:**
- Layout grid/flex
- Sidebar transitions
- Chat area styling
- Table display styling
- Modal overlay

### rag_ddbb.component.spec.ts

**Purpose:** Unit test suite for database RAG functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

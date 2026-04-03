# RAG PDF Screen

## Introduction

Screen for RAG (Retrieval Augmented Generation) with PDF documents. Provides chat interface for querying uploaded PDF collections with sidebar navigation, upload modal, and real-time response streaming via WebSocket.

## Files Documentation

### rag_pdf.component.ts

**Purpose:** Manages PDF RAG chat interface with collection management.

**Main Components:**
- `PdfComponent`: Standalone component implementing OnInit

**Properties:**
- `sidebarCollapsed`: Sidebar collapse state
- `collections`: Array of collection names
- `conversation`: Conversation history array
- `selectedCollection`: Currently selected collection
- `message/currentMessage`: Message input buffers
- `messages`: Chat message array with text, isUser, isTyping
- `isSending`: Sending state
- `mostrarModal`: Upload modal visibility

**Methods:**
- `abrirModal/cerrarModal()`: Modal management
- `toggleSidebar()`: Sidebar collapse toggle
- `loadCollections()`: Fetches collections from CollectionsService
- `renderConversation()`: Renders conversation history with markdown
- `selectCollection()`: Collection selection
- `deleteCollection()`: Collection deletion
- `onMessageChange()`: Message input change handler
- `sendMessage()`: Sends message via WebSocket with streaming
- `markdownRender()`: Converts markdown to SafeHtml
- `handleKeyPress()`: Enter key handler
- `scrollChatToBottom()`: Auto-scroll to latest message

**Dependencies:**
- `@angular/core`: Component, OnInit, ViewChild, ElementRef
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `@angular/forms`: FormsModule
- `@angular/platform-browser`: DomSanitizer, SafeHtml
- `marked`: Markdown parsing
- `CollectionsService`: PDF collection service
- Child components: UploadComponent, ChatOutputComponent, SidebarComponent, SidebarItemComponent, ButtonContainerComponent, UserInputComponent

**Integration:**
- Route: `/pdf` (protected by AuthGuard)
- WebSocket streaming via CollectionsService.sendMessage
- Opens upload modal when no collections exist

### rag_pdf.component.html

**Purpose:** Template for PDF RAG chat interface.

**Structure:**
- Container with sidebar and main content
- Sidebar with collection list
- Chat output area
- User input component
- Upload modal overlay

### rag_pdf.component.scss

**Purpose:** Styling for PDF RAG screen.

**Key Styles:**
- Layout grid/flex
- Sidebar transitions
- Chat area styling
- Modal overlay

### rag_pdf.component.spec.ts

**Purpose:** Unit test suite for PDF RAG functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

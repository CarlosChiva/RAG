# Excels Screen

## Introduction

Screen for RAG with Excel files. Provides chat interface for querying uploaded Excel files with sidebar navigation, upload modal, and real-time response streaming with thinking tokens support via WebSocket.

## Files Documentation

### excels.component.ts

**Purpose:** Manages Excel RAG chat interface with file management.

**Main Components:**
- `Excels`: Standalone component implementing OnInit

**Properties:**
- `conversation`: Conversation history
- `messages`: ChatMessage array with thinking tokens
- `currentBotMessageIndex`: Current bot message index
- `rawResponse`: Accumulated response text
- `collections`: Collections array
- `selectedCollection`: Selected Excel file
- `isSending`: Sending state
- `currentMessage/message`: Message input buffers
- `sidebarCollapsed`: Sidebar collapse state
- `mostrarModal`: Upload modal visibility
- `files`: Array of uploaded Excel files

**Methods:**
- `toggleSidebar()`: Sidebar collapse toggle
- `loadConfigs()`: Fetches files from ExcelService
- `selectCollection()`: File selection
- `renderConversation()`: Renders conversation with thinking tokens
- `deleteCollection()`: File deletion with list update
- `toggleShowFile()`: File visibility toggle
- `onMessageChange()`: Message input change
- `sendMessage()`: Sends query via WebSocket
- `handleIncoming()`: Processes WebSocket events
- `handleResponseEvent()`: Handles response/thinking events
- `appendToResponse()`: Appends text to response
- `markdownRender()`: Converts markdown to SafeHtml
- `abrirModal/cerrarModal()`: Modal management
- `onFileUploaded()`: Upload success handler
- `handleKeyPress()`: Enter key handler
- `scrollChatToBottom()`: Auto-scroll

**Dependencies:**
- `@angular/core`: Component, OnInit, ViewChild, ElementRef
- `@angular/common`: CommonModule
- `@angular/common/http`: HttpClientModule
- `@angular/router`: Router, RouterLink
- `@angular/platform-browser`: DomSanitizer, SafeHtml
- `marked`: Markdown parsing
- `ExcelService`: Excel service
- `ChatMessage`: Message interface
- Child components: SidebarComponent, SidebarExcelItemComponent, ChatOutputChatbotComponent, ButtonContainerComponent, UserInputComponent, ExcelUploaderComponent

**Integration:**
- Route: `/excel` (protected by AuthGuard)
- WebSocket streaming via ExcelService.sendMessage
- Opens upload modal when no files exist
- Supports thinking tokens display

### excels.component.html

**Purpose:** Template for Excel RAG chat interface.

**Structure:**
- Container with sidebar and main content
- Sidebar with file list
- Chat output area with thinking tokens
- User input component
- Upload modal overlay

### excels.component.scss

**Purpose:** Styling for Excel RAG screen.

**Key Styles:**
- Layout grid/flex
- Sidebar transitions
- Chat area styling
- Modal overlay

### excels.component.spec.ts

**Purpose:** Unit test suite for Excel RAG functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

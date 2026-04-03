# Chatbot Interaction Component

## Introduction

Structural base component that defines the chatbot screen layout template. Separates UI structure from business logic through a base class pattern, enabling code reuse across chatbot-related screens.

## Files Documentation

### chatbot-interaction.component.ts

**Purpose:** Template-only component defining the chatbot interaction layout.

**Main Components:**
- `ChatbotInteractionComponent`: Standalone component with embedded template

**Template Structure:**
- Fixed models list dropdown
- Collapsible sidebar with chat conversations
- Main chat area with output and input components
- Modal overlays for tool configuration (ComfyUI, MCP)

**Child Components Used:**
- `app-models-list`: Model selection dropdown
- `app-sidebar`: Collapsible sidebar container
- `app-sidebar-conversations-item`: Chat conversation list items
- `app-button-container`: Navigation controls
- `app-chat-output-chatbot`: Chat message display
- `app-user-input-chatbot`: User message input
- `app-upload-Comfy`: ComfyUI configuration modal
- `app-upload-mcp`: MCP configuration modal

**Integration:**
- Used as template base by `chatbot` screen
- No business logic - all functionality delegated to parent

### chatbot-interaction.component.scss

**Purpose:** Styling for chatbot interaction layout.

**Key Styles:**
- Container grid/flex layout
- Chat area responsive sizing
- Sidebar collapse/expand transitions
- Modal overlay positioning

### chatbot-interaction-base.ts

**Purpose:** Base class providing shared state and methods for chatbot interaction.

**Main Components:**
- `ChatbotInteractionBase`: Abstract base class implementing OnInit

**State Properties:**
- `sidebarCollapsed`: Sidebar visibility state
- `chats`: Array of available chat conversations
- `selectedChat`: Currently selected chat
- `currentMessage`: Input message buffer
- `isSending`: Message sending state
- `messages`: Chat message array
- `mcp_comfy_config`: Tool configuration object

**Methods:**
- `toggleSidebar()`: Toggles sidebar collapse state
- `onModelSelected()`: Model selection handler (to be implemented)
- `loadChats()`: Chat loading method (to be implemented)
- `renderConversation()`: Conversation rendering (to be implemented)
- `selectChat()`: Chat selection
- `deleteChat()`: Chat deletion (to be implemented)
- `onMessageChange()`: Message input change handler
- `openEditModal()`: Opens tool configuration modal
- `cerrarImageModal()`: Closes image configuration modal
- `cerrarMCPModal()`: Closes MCP configuration modal
- `scrollChatToBottom()`: Auto-scroll to latest message

**Dependencies:**
- `@angular/core`: Component, OnInit, ElementRef, ViewChild
- `@angular/common`: CommonModule
- Child components and interfaces

**Integration:**
- Inherited by child components that implement business logic

### chatbot-interaction.component.html

**Purpose:** (Embedded in TS file) Template defining chatbot layout structure.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

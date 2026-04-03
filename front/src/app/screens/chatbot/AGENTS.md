# Chatbot Screen

## Introduction

Advanced chatbot screen with model selection, conversation management, and tool integration (ComfyUI for image generation, MCP for external tools). Supports thinking tokens display, real-time response streaming, and conversation persistence.

## Files Documentation

### chatbot.component.ts

**Purpose:** Manages chatbot interface with model selection and tool configuration.

**Main Components:**
- `ChatbotComponent`: Standalone component implementing OnInit

**Properties:**
- `messages`: ChatMessage array with thinking tokens support
- `currentEditConfig`: Current tool configuration for editing
- `selectedModel`: Selected ModelItem
- `sidebarCollapsed`: Sidebar collapse state
- `chats/chat`: Available chat conversations
- `selectedChat`: Currently selected chat
- `message/currentMessage`: Message input buffers
- `isSending`: Sending state
- `mostrarImageModal/mostrarMCPModal`: Modal visibility states
- `rawResponse`: Accumulated response text
- `mcp_comfy_config`: Tool configuration object
- `config`: Query configuration (Config interface)
- `currentBotMessageIndex`: Current bot message index

**Methods:**
- `abrirImageModal/abrirMCPModal()`: Opens tool configuration modals
- `cerrarImageModal/cerrarMCPModal()`: Closes modals
- `toggleSidebar()`: Sidebar collapse toggle
- `onModelSelected()`: Model selection handler
- `loadChats()`: Fetches conversations from ModelsService
- `renderConversation()`: Renders conversation with thinking tokens
- `selectChat()`: Chat selection
- `deleteChat()`: Chat deletion
- `onMessageChange()`: Message input change
- `sendMessage()`: Sends query via WebSocket with tool support
- `openEditModal()`: Opens tool edit modal
- `handlChatbottMessage()`: Processes WebSocket events
- `handleResponseEvent()`: Handles response/thinking events
- `handleImageEvent()`: Handles image generation
- `appendToResponse()`: Appends text to response
- `markdownRender()`: Converts markdown to SafeHtml
- `handleKeyPress()`: Enter key handler
- `scrollChatToBottom()`: Auto-scroll
- `createChat()`: Creates new conversation
- `onToolConfigSelected()`: Tool configuration selection

**Dependencies:**
- `@angular/core`: Component, OnInit, ViewChild, ElementRef
- `@angular/common`: CommonModule
- `@angular/forms`: FormsModule
- `@angular/platform-browser`: DomSanitizer, SafeHtml
- `marked`: Markdown parsing
- `ModelsService`: Chatbot service
- Interfaces: Config, ToolConfigPayload, ModelItem, ChatMessage
- Child components: ChatOutputChatbotComponent, SidebarComponent, SidebarItemComponent, ButtonContainerComponent, ModelsListComponent, UserInputChatbotComponent, UploadComfyComponent, UploadMCPComponent

**Integration:**
- Route: `/chatbot` (protected by AuthGuard)
- WebSocket streaming via ModelsService.query
- Supports thinking tokens and image generation
- Manages tool configurations via modals

### chatbot.component.html

**Purpose:** Template for chatbot interface.

**Structure:**
- Container with sidebar and main content
- Model selection dropdown
- Sidebar with conversation list
- Chat output with thinking tokens
- User input with tool selection
- Tool configuration modals

### chatbot.component.scss

**Purpose:** Styling for chatbot screen.

**Key Styles:**
- Layout grid/flex
- Model dropdown positioning
- Thinking tokens display
- Image display styling
- Modal overlay

### chatbot.component.spec.ts

**Purpose:** Unit test suite for chatbot functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

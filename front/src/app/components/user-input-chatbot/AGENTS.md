# User Input Chatbot Component

## Introduction

Specialized user input component for the chatbot screen with tool configuration support. Provides message input with dropdown for selecting image generation (ComfyUI) or MCP tools before sending messages.

## Files Documentation

### user-input-chatbot.component.ts

**Purpose:** Manages user message input with tool configuration selection.

**Main Components:**
- `UserInputChatbotComponent`: Standalone component implementing OnInit

**Inputs:**
- `placeholder`: Input placeholder text
- `isSending`: Sending state for disable
- `disabled`: Input disabled state
- `sendButtonText`: Send button label
- `message`: Bidirectional message binding

**Outputs:**
- `messageChange`: Message change event
- `sendMessage`: Send message event
- `toolConfigSelected`: Tool configuration selection event
- `editToolConfig`: Tool configuration edit event

**Properties:**
- `dropdownDirection`: Dropdown positioning ('up' or 'down')
- `toolSelected`: Selected tool type
- `mcp_conf`: MCP configuration object
- `comfyui_conf`: ComfyUI configuration object
- `config_selected`: Selected configuration
- `isToolSelected`: Tool selection state
- `isDropdownOpen`: Dropdown visibility state

**Methods:**
- `loadConfigs()`: Loads tool configurations from ModelsService
- `hasImageConfig()`: Checks if ComfyUI config exists
- `hasMcpConfig()`: Checks if MCP config exists
- `onEditTool()`: Emits configuration for editing
- `onInputChange()`: Input change handler
- `onSendMessage()`: Send message handler
- `onKeyDown()`: Keyboard handler (Enter to send)
- `toggleToolSelected()`: Toggles tool selection state
- `toggleDropdown()`: Toggles dropdown with position detection
- `selectOption()`: Tool option selection with payload emission
- `onDocumentClick()`: Closes dropdown on outside click

**Dependencies:**
- `@angular/core`: Component, EventEmitter, HostListener, Input, OnInit, Output
- `@angular/common`: CommonModule
- `ModelsService`: Service for tool configuration API calls
- `ToolConfigPayload`: Configuration payload interface

**Integration:**
- Used in: `chatbot-interaction`, `chatbot` screen
- Loads and manages tool configurations
- Emits tool selection for message context

### user-input.component-chatbot.html

**Purpose:** Template for chatbot user input with tool dropdown.

**Structure:**
- Tool selection checkbox
- Dropdown button with menu
- Input field
- Send button

### user-input.component-chatbot.scss

**Purpose:** Styling for chatbot user input.

**Key Styles:**
- Input field styling
- Dropdown positioning
- Tool selection UI

### user-input-chatbot.component.spec.ts

**Purpose:** Unit test suite for chatbot user input functionality.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

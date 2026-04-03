# Chat Output Chatbot Component

## Introduction

Specialized chat output component for the chatbot screen that handles AI response rendering with thinking tokens support, markdown parsing, and scroll-to-bottom functionality. Displays both the AI's reasoning process and final response.

## Files Documentation

### chat-output-chatbot.component.ts

**Purpose:** Renders chat messages with support for thinking tokens and markdown formatting.

**Main Components:**
- `ChatMessage` interface: Defines message structure with thinking tokens, response text, event headers
- `ChatOutputChatbotComponent`: Standalone component implementing AfterViewChecked
- `toggleThinking()`: Toggles visibility of AI thinking process
- `hasThinkingTokens()`: Validates presence of thinking tokens
- `getThinkingText()`: Renders thinking tokens with markdown to SafeHtml
- `scrollToBottom()`: Auto-scrolls chat to latest message

**Dependencies:**
- `@angular/core`: Component, Input, ViewChild, ElementRef, AfterViewChecked
- `@angular/common`: CommonModule
- `@angular/platform-browser`: DomSanitizer, SafeHtml
- `marked`: Markdown parsing library

**Integration:**
- Receives `messages` array via @Input
- Sanitizes HTML content for security
- Used in: `chatbot-interaction`, `chatbot`, `excels` screens

### chat-output-chatbot.component.html

**Purpose:** Template for rendering chat messages with thinking/response separation.

**Structure:**
- Message list container with scroll
- Conditional rendering of thinking tokens
- Event header display
- Response text rendering

### chat-output-chatbot.component.scss

**Purpose:** Styling for chat output layout and message bubbles.

**Key Styles:**
- User vs AI message differentiation
- Thinking tokens collapsible section
- Scroll container styling

### chat-output-chatbot.component.spec.ts

**Purpose:** Unit test suite for chat output rendering.

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

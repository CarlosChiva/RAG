# Multimedia Screen

## Screen Name
`MultimediaScreen` - Video management and RAG interaction screen

## Description
A comprehensive screen that enables users to upload, play, and interact with video content using Retrieval-Augmented Generation (RAG). Combines video playback capabilities with AI-powered chat functionality, allowing users to ask questions about video content and maintain persistent conversations.

## Purpose
Provide an integrated interface for video-based RAG interactions, enabling users to:
- Upload and manage video files
- Play videos with custom controls
- Create and manage conversations about video content
- Interact with AI via chat to analyze or discuss video content
- Maintain conversation history for future reference

## Route
`/multimedia` (protected by JWT authentication)

## Features

### 1. Video Management
- Upload video files via file input
- Store videos on backend server
- Retrieve video URLs for playback
- Delete videos when needed

### 2. Video Playback
- Integrated VideoPlayerComponent with custom controls
- Play/pause, seek, volume control, fullscreen
- Error handling and loading states
- Playback state tracking

### 3. Conversation Management
- List all video-related conversations
- Create new conversations
- Load existing conversations
- Delete conversations
- Associate videos with conversations

### 4. Chat Interface
- Real-time messaging with AI via WebSocket
- Markdown rendering for AI responses
- Thinking tokens display
- Streaming response with `__END__` marker
- Message history persistence

### 5. Sidebar Navigation
- Collapsible sidebar with conversation list
- Video upload section
- Quick navigation between conversations
- Create new chat button

## Components Used

| Component | Purpose |
|-----------|---------|
| `VideoPlayerComponent` | Video playback with custom controls |
| `SidebarComponent` | Left sidebar container with navigation |
| `SidebarItemComponent` | Conversation list items in sidebar |
| `ChatOutputChatbotComponent` | Chat message display with markdown rendering |
| `UserInputChatbotComponent` | Text input for user messages |
| `ButtonContainerComponent` | Action buttons (send, clear, save) |

## State Management

### State Properties
| Property | Type | Description |
|----------|------|-------------|
| `conversations` | `any[]` | List of all available conversations |
| `currentConversation` | `any` | Currently loaded conversation object |
| `selectedVideo` | `File \| null` | Currently selected video file |
| `videoUrl` | `string \| null` | URL of video to play |
| `sidebarCollapsed` | `boolean` | Sidebar visibility state |
| `chat` | `any[]` | Chat messages array |
| `selectedChat` | `string \| null` | ID of selected conversation |
| `message` | `string` | Current input message |
| `currentMessage` | `string` | Message from input component |
| `isSending` | `boolean` | Message sending state |
| `rawResponse` | `string` | Accumulated AI response text |
| `messages` | `ChatMessage[]` | Display messages array |

### Child Component References
| ViewChild | Type | Description |
|-----------|------|-------------|
| `chatOutput` | `ElementRef` | Chat output container for scrolling |
| `inputText` | `ElementRef` | Input field reference |
| `chatOutputComponent` | `ChatOutputChatbotComponent` | Chat output component instance |
| `sidebarComponent` | `SidebarComponent` | Sidebar component instance |
| `videoPlayerComponent` | `VideoPlayerComponent` | Video player component instance |

## Methods

### Sidebar Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `toggleSidebar()` | - | Toggle sidebar collapsed/expanded state |

### Conversation Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `loadConversations()` | - | Fetch list of conversations from backend |
| `loadConversation(conversationId: string)` | `conversationId` | Load specific conversation and render messages |
| `renderConversation(conversation: any)` | `conversation` | Convert conversation messages to ChatMessage format |
| `selectChat(chat: string)` | `chat` | Select a conversation by ID |
| `deleteChat(conversationId: string)` | `conversationId` | Delete conversation and refresh list |
| `createChat(event?: Event)` | `event` | Create new conversation with unique name |

### Video Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `handleVideoUpload(event: any)` | `event` | Handle file input change event |
| `uploadVideo(file: File)` | `file` | Upload video file to backend |
| `playVideo()` | - | Play current video via VideoPlayerComponent |
| `onVideoEnded()` | - | Handle video ended event |
| `onPlaybackStateChanged(state: PlaybackState)` | `state` | Handle playback state changes |

### Message Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `onMessageChange(message: string)` | `message` | Update current message from input |
| `sendMessage(messageFromChild?: string)` | `messageFromChild` | Send message via WebSocket |
| `handleMultimediaMessage(data: any)` | `data` | Process WebSocket message |
| `handleResponseEvent(data: any, currentMessage: ChatMessage)` | `data, currentMessage` | Handle AI response events |
| `appendToResponse(data: any, currentMessage: ChatMessage)` | `data, currentMessage` | Append text to response |
| `markdownRender(message: string)` | `message` | Convert markdown to HTML |
| `handleKeyPress(event: KeyboardEvent)` | `event` | Handle Enter key to send |
| `scrollChatToBottom()` | - | Scroll chat to bottom (private) |

## Integration with multimedia.service

The screen consumes `MultimediaService` for all backend operations:

```typescript
constructor(
  private multimediaService: MultimediaService,
  private sanitizer: DomSanitizer,
) {}
```

### Service Method Calls
| Screen Method | Service Method | Purpose |
|---------------|----------------|---------|
| `loadConversations()` | `listConversations()` | GET /api/conversations |
| `uploadVideo()` | `uploadVideo()` | POST /api/upload (multipart) |
| `loadConversation()` | `getConversation()` | GET /api/conversations/{id} |
| `createChat()` | `createConversation()` | POST /api/conversations |
| `deleteChat()` | `deleteConversation()` | DELETE /api/conversations/{id} |
| `sendMessage()` | `sendMessage()` | WebSocket ws://localhost:8006/api/chat |

## Authentication
- **Type:** JWT (JSON Web Token)
- **Storage:** `localStorage.getItem('access_token')`
- **Header:** `Authorization: Bearer <token>`
- **Protection:** Route protected by `AuthGuard`

## Usage Flow

### 1. Initial Load
```
User navigates to /multimedia
    ↓
ngOnInit() → loadConversations()
    ↓
multimediaService.listConversations()
    ↓
Display conversation list in sidebar
```

### 2. Upload and Play Video
```
User selects video file
    ↓
handleVideoUpload(event)
    ↓
uploadVideo(file)
    ↓
multimediaService.uploadVideo(file)
    ↓
Backend returns { url: '...' }
    ↓
Set videoUrl = response.url
    ↓
VideoPlayerComponent loads video
    ↓
User clicks play button
    ↓
playVideo() → videoPlayerComponent.play()
```

### 3. Create Conversation and Chat
```
User clicks "New Chat" button
    ↓
createChat()
    ↓
multimediaService.createConversation(name)
    ↓
Backend creates conversation
    ↓
Set currentConversation and selectedChat
    ↓
User types message
    ↓
sendMessage()
    ↓
Add user message to messages array
    ↓
multimediaService.sendMessage(conversationId, message, callback)
    ↓
WebSocket streaming with callback
    ↓
handleMultimediaMessage(data) processes each message
    ↓
Render AI response with markdown
```

### 4. Load Existing Conversation
```
User clicks conversation in sidebar
    ↓
loadConversation(conversationId)
    ↓
multimediaService.getConversation(conversationId)
    ↓
renderConversation(conversation)
    ↓
Convert messages to ChatMessage format
    ↓
Display in chat output
```

## WebSocket Message Handling

The screen handles structured WebSocket messages:

```typescript
handleMultimediaMessage(data: any): void {
  if (data.event) {
    switch (data.event) {
      case 'response':
        this.handleResponseEvent(data, currentMessage);
        break;
      default:
        currentMessage.eventHeader = data.event;
    }
  } else {
    this.appendToResponse(data, currentMessage);
  }
}
```

### Message Types
| Event | Step | Data | Action |
|-------|------|------|--------|
| `response` | `thinking` | `token` | Add to thinkingTokens array |
| `response` | `response` | `response` | Append to responseText with markdown |
| Other | - | - | Update eventHeader |

## Message Rendering

User messages are displayed as-is, while AI messages undergo processing:

```typescript
renderConversation(conversation: any): void {
  const messages = conversation.messages || [];
  
  this.messages = messages.map((msg: any) => {
    if ('user' in msg) {
      return { text: msg.user, isUser: true, ... } as ChatMessage;
    }
    if ('bot' in msg) {
      const botText: string = msg.bot;
      const thinkingTokens: string[] = [];
      
      const remainingText = botText.replace(/<think>(.*?)<\/think>/gs, (match, p1) => {
        thinkingTokens.push(p1);
        return '';
      }).trim();
      
      const renderedContent = this.markdownRender(remainingText);
      
      return {
        text: '',
        isUser: false,
        thinkingTokens: thinkingTokens,
        responseText: renderedContent,
        showThinking: true,
        ...
      } as ChatMessage;
    }
  });
}
```

## Dependencies
- `@angular/core`: Component, OnInit, ElementRef, ViewChild
- `@angular/common`: CommonModule
- `@angular/forms`: FormsModule
- `@angular/platform-browser`: DomSanitizer, SafeHtml
- `marked`: Markdown parsing
- Local components: `ChatOutputChatbotComponent`, `SidebarComponent`, `SidebarItemComponent`, `ButtonContainerComponent`, `UserInputChatbotComponent`, `VideoPlayerComponent`
- Local services: `MultimediaService`
- Local interfaces: `ChatMessage`

## Files
- `multimedia.screen.ts` - Screen component logic
- `multimedia.screen.html` - Template
- `multimedia.screen.scss` - Styles
- `AGENTS.md` - This documentation

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

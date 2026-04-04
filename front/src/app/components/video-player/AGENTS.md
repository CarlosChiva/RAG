# Video Player Component

## Component Name
`VideoPlayerComponent` - Reusable HTML5 video player with custom controls

## Description
A fully-featured, reusable video player component designed for the RAG multimedia screen. Provides custom playback controls, error handling, loading states, fullscreen support, and responsive design consistent with the project's dark theme aesthetic.

## Purpose
Enable video playback and control within the multimedia RAG interface, supporting integration with video-based conversations and LLM interactions.

## Technical Details

### Component Metadata
- **Selector:** `app-video-player`
- **Standalone:** true
- **Imports:** `CommonModule`
- **Lifecycle Hooks:** `AfterViewInit`, `OnDestroy`, `OnChanges`

### Inputs
| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `videoUrl` | `string` | - | **Required** URL or blob URL of the video to play |
| `autoPlay` | `boolean` | `false` | Automatically play video when loaded |
| `conversationId` | `string` | - | Optional conversation ID for tracking |

### Outputs
| Output | Type | Description |
|--------|------|-------------|
| `videoEnded` | `EventEmitter<void>` | Emits when video playback ends |
| `playbackStateChanged` | `EventEmitter<PlaybackState>` | Emits when playback state changes ('playing' \| 'paused' \| 'ended') |

### Public Methods
| Method | Parameters | Description |
|--------|------------|-------------|
| `play()` | - | Start/resume video playback |
| `pause()` | - | Pause video playback |
| `seekTo(time: number)` | `time: number` | Seek to specific time in seconds |
| `setVolume(level: number)` | `level: number (0-1)` | Set volume level |
| `toggleMute()` | - | Toggle mute state |
| `toggleFullscreen()` | - | Enter/exit fullscreen mode |
| `reloadVideo()` | - | Reload the current video |

### State Properties (Internal)
| Property | Type | Description |
|----------|------|-------------|
| `isLoading` | `boolean` | Video loading state |
| `isError` | `boolean` | Error state |
| `isPlaying` | `boolean` | Current playback state |
| `currentTime` | `number` | Current playback position in seconds |
| `duration` | `number` | Total video duration in seconds |
| `volume` | `number` | Current volume (0-1) |
| `isMuted` | `boolean` | Mute state |
| `errorMessage` | `string` | Error description |
| `isBuffering` | `boolean` | Buffering state |
| `isFullscreen` | `boolean` | Fullscreen state |

## Features

### 1. Custom Controls
- Play/Pause button with dynamic icon (▶️/⏸️)
- Progress bar with click-to-seek functionality
- Time display (current / total)
- Volume slider with mute toggle (🔇/🔊)
- Fullscreen toggle (⛶/☐)

### 2. Error Handling
- Network error detection and display
- Format support validation
- Corrupted file handling
- Auto-play prevention handling
- Retry button on error

### 3. Loading States
- Loading overlay with spinner
- Buffering indicator during playback
- Metadata preloading for faster start

### 4. Fullscreen Support
- Native fullscreen API integration
- Fullscreen state tracking
- Custom controls visible in fullscreen

### 5. Responsive Design
- Fluid container sizing
- Controls adapt to container width
- Consistent with project dark theme

### 6. Accessibility
- ARIA labels on all controls
- Keyboard navigation support
- Semantic HTML structure

## Usage Example

### Template
```html
<app-video-player
  [videoUrl]="videoUrl"
  [autoPlay]="false"
  [conversationId]="currentConversation?.id"
  (videoEnded)="onVideoEnded()"
  (playbackStateChanged)="onPlaybackStateChanged($event)">
</app-video-player>
```

### Component TypeScript
```typescript
import { VideoPlayerComponent, PlaybackState } from '../../components/video-player/video-player.component';

export class MultimediaScreen {
  @ViewChild(VideoPlayerComponent) videoPlayerComponent!: VideoPlayerComponent;
  
  videoUrl: string | null = null;
  
  // Control video programmatically
  playVideo(): void {
    if (this.videoUrl && this.videoPlayerComponent) {
      this.videoPlayerComponent.play();
    }
  }
  
  onVideoEnded(): void {
    console.log('Video ended');
  }
  
  onPlaybackStateChanged(state: PlaybackState): void {
    console.log('Playback state:', state);
  }
}
```

## HTML5 Video API Integration

The component wraps the native HTML5 Video API with Angular's `ElementRef`:

```typescript
@ViewChild('videoElement') videoElement!: ElementRef<HTMLVideoElement>;

// Direct access to video methods
play() {
  this.videoElement.nativeElement.play();
}

// Event listeners
video.addEventListener('play', () => this.onPlay());
video.addEventListener('pause', () => this.onPause());
video.addEventListener('ended', () => this.onEnded());
video.addEventListener('timeupdate', () => this.onTimeUpdate());
video.addEventListener('error', (e) => this.onError(e));
```

## Lifecycle Management

### AfterViewInit
- Initializes video element event listeners
- Sets up fullscreen change detection

### OnChanges
- Detects `videoUrl` changes
- Automatically reloads video when URL changes

### OnDestroy
- Pauses video playback
- Clears video source
- Prevents memory leaks

## Style Information

### Design System
- **Theme:** Dark (consistent with project styles)
- **Background:** Gradient (#504f4f → #333)
- **Text Color:** #e0e0e0 (light gray)
- **Control Bar:** Semi-transparent dark background
- **Progress Bar:** Accent color with buffered overlay

### CSS Classes
- `.video-player-container`: Main container
- `.loading-overlay`: Loading state overlay
- `.error-overlay`: Error state overlay
- `.buffering-indicator`: Buffering spinner
- `.custom-controls`: Controls container
- `.progress-container`: Progress bar area
- `.controls-bar`: Button bar
- `.control-button`: Individual control button

## Event Flow

```
Video URL Change
    ↓
reloadVideo()
    ↓
video.load()
    ↓
loadeddata event → isLoading = false
    ↓
autoPlay = true → video.play()
    ↓
play event → isPlaying = true → playbackStateChanged.emit('playing')
    ↓
Playback...
    ↓
ended event → isPlaying = false → videoEnded.emit() → playbackStateChanged.emit('ended')
```

## Error Codes Handling

| Code | Constant | Message |
|------|----------|---------|
| 1 | MEDIA_ERR_ABORTED | "Video loading was aborted" |
| 2 | MEDIA_ERR_NETWORK | "Network error while loading video" |
| 3 | MEDIA_ERR_DECODE | "Video format not supported or corrupted" |
| 4 | MEDIA_ERR_SRC_NOT_SUPPORTED | "Video source not supported" |

## Dependencies
- `@angular/core`: Component, Input, Output, EventEmitter, ElementRef, ViewChild, AfterViewInit, OnDestroy, OnChanges
- `@angular/common`: CommonModule

## Files
- `video-player.component.ts` - Component logic
- `video-player.component.html` - Template
- `video-player.component.scss` - Styles
- `AGENTS.md` - This documentation

---

**Parent Directory:** [./AGENTS.md](./AGENTS.md)

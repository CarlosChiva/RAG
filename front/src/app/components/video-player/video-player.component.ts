import { Component, Input, Output, EventEmitter, ElementRef, ViewChild, AfterViewInit, OnDestroy, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

export type PlaybackState = 'playing' | 'paused' | 'ended';

@Component({
  selector: 'app-video-player',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './video-player.component.html',
  styleUrls: ['./video-player.component.scss']
})
export class VideoPlayerComponent implements AfterViewInit, OnDestroy, OnChanges {
  @Input() videoUrl!: string;
  @Input() autoPlay: boolean = false;
  @Input() conversationId?: string | null;

  @Output() videoEnded = new EventEmitter<void>();
  @Output() playbackStateChanged = new EventEmitter<PlaybackState>();

  @ViewChild('videoElement') videoElement!: ElementRef<HTMLVideoElement>;

  // State tracking
  isLoading: boolean = false;
  isError: boolean = false;
  isPlaying: boolean = false;
  currentTime: number = 0;
  duration: number = 0;
  volume: number = 1;
  isMuted: boolean = false;
  errorMessage: string = '';
  isBuffering: boolean = false;
  isFullscreen: boolean = false;

  ngAfterViewInit(): void {
    this.initializeVideo();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['videoUrl'] && changes['videoUrl'].currentValue !== changes['videoUrl'].previousValue) {
      this.reloadVideo();
    }
  }

  ngOnDestroy(): void {
    if (this.videoElement?.nativeElement) {
      const video = this.videoElement.nativeElement;
      video.pause();
      video.src = '';
      video.load();
    }
  }

  private initializeVideo(): void {
    if (this.videoElement?.nativeElement) {
      const video = this.videoElement.nativeElement;
      
      // Event listeners
      video.addEventListener('play', () => this.onPlay());
      video.addEventListener('pause', () => this.onPause());
      video.addEventListener('ended', () => this.onEnded());
      video.addEventListener('timeupdate', () => this.onTimeUpdate());
      video.addEventListener('error', (e) => this.onError(e));
      video.addEventListener('loadeddata', () => this.onLoadedData());
      video.addEventListener('waiting', () => this.onWaiting());
      video.addEventListener('canplay', () => this.onCanPlay());
      
      // Fullscreen event
      document.addEventListener('fullscreenchange', () => this.onFullscreenChange());
    }
  }

  reloadVideo(): void {
    if (this.videoElement?.nativeElement) {
      const video = this.videoElement.nativeElement;
      video.pause();
      video.src = this.videoUrl;
      video.load();
      
      this.currentTime = 0;
      this.duration = 0;
      this.isError = false;
      this.errorMessage = '';
      this.isLoading = true;
      
      if (this.autoPlay && this.videoUrl) {
        video.play().catch(err => {
          console.error('Auto-play failed:', err);
          this.isError = true;
          this.errorMessage = 'Auto-play was prevented. Please press play.';
        });
      }
    }
  }

  private onPlay(): void {
    this.isPlaying = true;
    this.playbackStateChanged.emit('playing');
  }

  private onPause(): void {
    this.isPlaying = false;
    this.playbackStateChanged.emit('paused');
  }

  private onEnded(): void {
    this.isPlaying = false;
    this.currentTime = 0;
    this.videoEnded.emit();
    this.playbackStateChanged.emit('ended');
  }

  private onTimeUpdate(): void {
    if (this.videoElement?.nativeElement) {
      this.currentTime = this.videoElement.nativeElement.currentTime;
    }
  }

  private onError(event: Event): void {
    const video = (event.target as HTMLVideoElement);
    this.isError = true;
    this.isLoading = false;
    
    let errorMsg = 'Error loading video';
    if (video.error) {
      switch (video.error.code) {
        case 1: // MEDIA_ERR_ABORTED
          errorMsg = 'Video loading was aborted';
          break;
        case 2: // MEDIA_ERR_NETWORK
          errorMsg = 'Network error while loading video';
          break;
        case 3: // MEDIA_ERR_DECODE
          errorMsg = 'Video format not supported or corrupted';
          break;
        case 4: // MEDIA_ERR_SRC_NOT_SUPPORTED
          errorMsg = 'Video source not supported';
          break;
      }
    }
    this.errorMessage = errorMsg;
  }

  private onLoadedData(): void {
    if (this.videoElement?.nativeElement) {
      this.duration = this.videoElement.nativeElement.duration;
    }
    this.isLoading = false;
  }

  private onWaiting(): void {
    this.isBuffering = true;
  }

  private onCanPlay(): void {
    this.isBuffering = false;
    this.isLoading = false;
  }

  private onFullscreenChange(): void {
    this.isFullscreen = document.fullscreenElement !== null;
  }

  // Public methods
  play(): void {
    if (this.videoElement?.nativeElement) {
      this.videoElement.nativeElement.play().catch(err => {
        console.error('Play error:', err);
        this.isError = true;
        this.errorMessage = 'Unable to play video';
      });
    }
  }

  pause(): void {
    if (this.videoElement?.nativeElement) {
      this.videoElement.nativeElement.pause();
    }
  }

  seekTo(time: number): void {
    if (this.videoElement?.nativeElement) {
      const video = this.videoElement.nativeElement;
      time = Math.max(0, Math.min(time, video.duration || 0));
      video.currentTime = time;
    }
  }

  setVolume(level: number): void {
    if (this.videoElement?.nativeElement) {
      const video = this.videoElement.nativeElement;
      this.volume = Math.max(0, Math.min(1, level));
      video.volume = this.volume;
      this.isMuted = this.volume === 0;
    }
  }

  toggleMute(): void {
    if (this.videoElement?.nativeElement) {
      this.isMuted = !this.isMuted;
      this.videoElement.nativeElement.muted = this.isMuted;
      if (this.isMuted) {
        this.volume = this.videoElement.nativeElement.volume;
        this.videoElement.nativeElement.volume = 0;
      } else {
        this.videoElement.nativeElement.volume = this.volume;
      }
    }
  }

  toggleFullscreen(): void {
    if (!document.fullscreenElement) {
      this.videoElement?.nativeElement.requestFullscreen().catch(err => {
        console.error('Fullscreen error:', err);
      });
    } else {
      document.exitFullscreen();
    }
  }

  onProgressClick(event: MouseEvent): void {
    const progressBar = event.currentTarget as HTMLElement;
    const rect = progressBar.getBoundingClientRect();
    const percentage = (event.clientX - rect.left) / rect.width;
    const time = percentage * this.duration;
    this.seekTo(time);
  }

  formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  get progressPercentage(): number {
    if (this.duration === 0) return 0;
    return (this.currentTime / this.duration) * 100;
  }

  get bufferedPercentage(): number {
    if (this.videoElement?.nativeElement && this.duration > 0) {
      const video = this.videoElement.nativeElement;
      if (video.buffered.length > 0) {
        const bufferedEnd = video.buffered.end(video.buffered.length - 1);
        return Math.min((bufferedEnd / this.duration) * 100, 100);
      }
    }
    return 0;
  }

  onSeekInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    const percentage = parseFloat(input.value);
    const time = (percentage / 100) * this.duration;
    this.seekTo(time);
  }
}

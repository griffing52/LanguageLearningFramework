/**
 * Audio service - audio playback management
 */

export class AudioService {
  private audioElement: HTMLAudioElement | null = null;
  private isPlaying = false;

  /**
   * Play audio from URL
   */
  async play(audioUrl: string): Promise<void> {
    if (!audioUrl) {
      console.warn('No audio URL provided');
      return;
    }

    try {
      if (!this.audioElement) {
        this.audioElement = new Audio();
      }

      this.audioElement.src = audioUrl;
      this.isPlaying = true;
      await this.audioElement.play();
    } catch (error) {
      console.error('Error playing audio:', error);
      this.isPlaying = false;
    }
  }

  /**
   * Stop current audio
   */
  stop(): void {
    if (this.audioElement) {
      this.audioElement.pause();
      this.audioElement.currentTime = 0;
      this.isPlaying = false;
    }
  }

  /**
   * Check if audio is playing
   */
  getIsPlaying(): boolean {
    return this.isPlaying;
  }

  /**
   * Set up completion callback
   */
  onComplete(callback: () => void): void {
    if (this.audioElement) {
      this.audioElement.addEventListener('ended', () => {
        this.isPlaying = false;
        callback();
      });
    }
  }
}

export const audioService = new AudioService();

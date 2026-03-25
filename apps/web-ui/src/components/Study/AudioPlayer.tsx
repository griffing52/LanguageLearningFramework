/**
 * Audio Player component
 */

import React, { useState, useEffect } from 'react';
import { audioService } from '@/services/audioService';
import '@/styles/components.css';

interface AudioPlayerProps {
  audioUrl?: string;
  label?: string;
  autoPlay?: boolean;
  onPlay?: () => void;
  onEnded?: () => void;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({
  audioUrl,
  label = 'Play Audio',
  autoPlay = false,
  onPlay,
  onEnded
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (onEnded) {
      audioService.onComplete(onEnded);
    }
  }, [onEnded]);

  useEffect(() => {
    if (autoPlay && audioUrl) {
      void handlePlay();
    }
  }, [autoPlay, audioUrl]);

  const handlePlay = async () => {
    if (!audioUrl) return;

    try {
      setIsLoading(true);
      await audioService.play(audioUrl);
      setIsPlaying(true);
      onPlay?.();
    } catch (error) {
      console.error('Error playing audio:', error);
      setIsPlaying(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = () => {
    audioService.stop();
    setIsPlaying(false);
  };

  if (!audioUrl) {
    return <div className="audio-player disabled">No audio available</div>;
  }

  return (
    <div className="audio-player">
      <button
        className={`audio-button ${isPlaying ? 'playing' : ''}`}
        onClick={isPlaying ? handleStop : handlePlay}
        disabled={isLoading}
      >
        {isLoading ? '⏳ Loading...' : isPlaying ? '⏹ Stop' : '▶ ' + label}
      </button>
    </div>
  );
};

/**
 * Study Card - Complete study item interface
 */

import React from 'react';
import { StudyTarget } from '@/api/study';
import { WordDisplay } from './WordDisplay';
import { AudioPlayer } from './AudioPlayer';
import { FeedbackUI } from './FeedbackUI';
import '@/styles/components.css';

interface StudyCardProps {
  target: StudyTarget;
  onFeedback: (correct: boolean, confidence: number, timeSpent: number) => Promise<void>;
  onSkip?: () => void;
  isLoading?: boolean;
}

export const StudyCard: React.FC<StudyCardProps> = ({
  target,
  onFeedback,
  onSkip,
  isLoading = false
}) => {
  return (
    <div className="study-card">
      <div className="study-content">
        <WordDisplay target={target} />
        
        <div className="study-controls">
          <AudioPlayer
            audioUrl={target.audio_url}
            label="Pronounce"
            onPlay={() => console.log('Playing audio')}
          />
        </div>
      </div>

      <div className="study-response">
        <FeedbackUI
          onSubmit={onFeedback}
          onSkip={onSkip}
          disabled={isLoading}
        />
      </div>
    </div>
  );
};

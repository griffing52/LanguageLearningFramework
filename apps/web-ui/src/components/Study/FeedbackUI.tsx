/**
 * Study Feedback component - for recording responses
 */

import React, { useState } from 'react';
import '@/styles/components.css';

interface FeedbackUIProps {
  onSubmit: (correct: boolean, confidence: number, timeSpent: number) => Promise<void>;
  onSkip?: () => void;
  disabled?: boolean;
}

export const FeedbackUI: React.FC<FeedbackUIProps> = ({ 
  onSubmit, 
  onSkip,
  disabled = false 
}) => {
  const [confidence, setConfidence] = useState(3);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [timeStart] = useState(Date.now());

  const handleCorrect = async () => {
    setIsSubmitting(true);
    try {
      const timeSpent = Math.round((Date.now() - timeStart) / 1000);
      await onSubmit(true, confidence, timeSpent);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleIncorrect = async () => {
    setIsSubmitting(true);
    try {
      const timeSpent = Math.round((Date.now() - timeStart) / 1000);
      await onSubmit(false, confidence, timeSpent);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="feedback-ui">
      <div className="confidence-selector">
        <label>How confident are you?</label>
        <div className="confidence-scale">
          {[1, 2, 3, 4, 5].map(level => (
            <button
              key={level}
              className={`confidence-btn ${confidence === level ? 'active' : ''}`}
              onClick={() => setConfidence(level)}
              disabled={disabled}
              title={
                level === 1 ? 'Very unsure' :
                level === 2 ? 'Unsure' :
                level === 3 ? 'Neutral' :
                level === 4 ? 'Pretty sure' :
                'Very sure'
              }
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      <div className="feedback-buttons">
        <button
          className="btn btn-success"
          onClick={handleCorrect}
          disabled={disabled || isSubmitting}
        >
          ✓ Correct
        </button>
        <button
          className="btn btn-error"
          onClick={handleIncorrect}
          disabled={disabled || isSubmitting}
        >
          ✗ Incorrect
        </button>
        {onSkip && (
          <button
            className="btn btn-secondary"
            onClick={onSkip}
            disabled={disabled || isSubmitting}
          >
            ⊘ Skip
          </button>
        )}
      </div>
    </div>
  );
};

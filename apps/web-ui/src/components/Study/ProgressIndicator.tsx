/**
 * Progress indicator component
 */

import React from 'react';
import '@/styles/components.css';

interface ProgressIndicatorProps {
  current: number;
  total: number;
  isComplete?: boolean;
}

export const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({
  current,
  total,
  isComplete = false
}) => {
  const percentage = total > 0 ? Math.round((current / total) * 100) : 0;

  return (
    <div className="progress-indicator">
      <div className="progress-header">
        <span className="progress-text">
          {current} of {total}
        </span>
        {isComplete && <span className="completion-badge">✓ Complete!</span>}
      </div>
      
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      
      <div className="progress-percentage">{percentage}%</div>
    </div>
  );
};

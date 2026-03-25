/**
 * Word Display component - shows word/phrase with translation
 */

import React from 'react';
import { StudyTarget } from '@/api/study';
import '@/styles/components.css';

interface WordDisplayProps {
  target: StudyTarget;
}

export const WordDisplay: React.FC<WordDisplayProps> = ({ target }) => {
  const isPhrase = target.target_type === 'phrase';

  return (
    <div className={`word-display ${isPhrase ? 'phrase' : 'word'}`}>
      <div className="word-container">
        <h2 className="word-value">{target.target_value}</h2>
        
        <div className="word-meta">
          <span className="item-type">
            {isPhrase ? '📝 Phrase' : '💬 Word'}
          </span>
          <span className="urgency">
            {target.urgency_score > 0.8 ? '🔴 Urgent' : 
             target.urgency_score > 0.5 ? '🟡 Soon' : 
             '🟢 Ready'}
          </span>
        </div>

        <div className="translation-divider">—</div>

        <p className="translation">{target.target_translation}</p>

        <div className="reason">
          <small>{target.reason}</small>
        </div>
      </div>
    </div>
  );
};

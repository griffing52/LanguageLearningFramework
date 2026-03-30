/**
 * Word List component
 */

import React, { useState, useEffect } from 'react';
import { vocabularyApi, Word } from '@/api/vocabulary';
import '@/styles/components.css';

interface WordListProps {
  limit?: number;
}

export const WordList: React.FC<WordListProps> = ({ limit = 50 }) => {
  const [words, setWords] = useState<Word[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const loadWords = async () => {
      setIsLoading(true);
      try {
        const result = await vocabularyApi.getWords(1, limit, searchQuery);
        setWords(result.words || []);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load words');
      } finally {
        setIsLoading(false);
      }
    };

    const timer = setTimeout(loadWords, 300); // Debounce search
    return () => clearTimeout(timer);
  }, [searchQuery, limit]);

  return (
    <div className="word-list">
      <div className="list-header">
        <h3>Vocabulary</h3>
        <input
          type="text"
          className="search-input"
          placeholder="Search words..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {isLoading && <div className="loading">Loading...</div>}
      {error && <div className="error-message">{error}</div>}

      {!isLoading && words.length === 0 && (
        <div className="empty-state">No words found</div>
      )}

      <div className="word-grid">
        {words.map((word) => (
          <div key={word.value} className="word-item">
            <div className="word-value">{word.value}</div>
            <div className="word-translation">{word.translation}</div>
            <div className="word-stats">
              <span title="Frequency">Freq: {word.frequency}</span>
              <span title="Complexity">Complex: {word.complexity}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

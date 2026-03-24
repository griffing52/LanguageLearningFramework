/**
 * Dashboard component - Learning progress overview
 */

import React, { useState, useEffect } from 'react';
import { progressApi, DetailedProgress } from '@/api/progress';
import '../styles/components.css';

export const Dashboard: React.FC = () => {
  const [progress, setProgress] = useState<DetailedProgress | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProgress = async () => {
      setIsLoading(true);
      try {
        const data = await progressApi.getDetailed();
        setProgress(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load progress');
      } finally {
        setIsLoading(false);
      }
    };

    loadProgress();
    const interval = setInterval(loadProgress, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  if (isLoading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!progress) return <div className="empty-state">No progress data</div>;

  const getMilestoneEmoji = (achieved: boolean) => achieved ? '✅' : '⭕';

  return (
    <div className="dashboard">
      <h2>Learning Progress</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Vocabulary</h3>
          <div className="stat-value">{progress.vocabulary.words_learned}</div>
          <div className="stat-label">of {progress.vocabulary.total_words} words</div>
          <div className="progress-mini">
            <div
              className="progress-fill"
              style={{ width: `${progress.vocabulary.words_percentage}%` }}
            />
          </div>
          <div className="stat-percentage">{progress.vocabulary.words_percentage}%</div>
        </div>

        <div className="stat-card">
          <h3>Phrases</h3>
          <div className="stat-value">{progress.phrases.phrases_learned}</div>
          <div className="stat-label">of {progress.phrases.total_phrases} phrases</div>
          <div className="progress-mini">
            <div
              className="progress-fill"
              style={{ width: `${progress.phrases.phrases_percentage}%` }}
            />
          </div>
          <div className="stat-percentage">{progress.phrases.phrases_percentage}%</div>
        </div>

        <div className="stat-card">
          <h3>Overall</h3>
          <div className="stat-value">{progress.overall.items_learned}</div>
          <div className="stat-label">of {progress.overall.total_items} total</div>
          <div className="progress-mini">
            <div
              className="progress-fill"
              style={{ width: `${progress.overall.items_percentage}%` }}
            />
          </div>
          <div className="stat-percentage">{progress.overall.items_percentage}%</div>
        </div>
      </div>

      <div className="milestones">
        <h3>🏆 Milestones</h3>
        <div className="milestone-list">
          <div className="milestone">
            {getMilestoneEmoji(progress.milestones.first_words)} First Words (10+)
          </div>
          <div className="milestone">
            {getMilestoneEmoji(progress.milestones.first_phrases)} First Phrases (5+)
          </div>
          <div className="milestone">
            {getMilestoneEmoji(progress.milestones.quarter_vocabulary)} Quarter Learned (25%)
          </div>
          <div className="milestone">
            {getMilestoneEmoji(progress.milestones.half_vocabulary)} Half Learned (50%)
          </div>
          <div className="milestone">
            {getMilestoneEmoji(progress.milestones.nearly_done)} Nearly Done (90%)
          </div>
        </div>
      </div>
    </div>
  );
};

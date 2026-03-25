/**
 * Progress API endpoints
 */

import { apiClient } from './client';
import { config } from '@/config';

export interface ProgressSnapshot {
  total_words: number;
  words_learned: number;
  total_phrases: number;
  phrases_learned: number;
  average_complexity: number;
  session_count: number;
  last_session_time?: string;
}

export interface DetailedProgress {
  vocabulary: {
    total_words: number;
    words_learned: number;
    words_percentage: number;
    words_remaining: number;
  };
  phrases: {
    total_phrases: number;
    phrases_learned: number;
    phrases_percentage: number;
    phrases_remaining: number;
  };
  overall: {
    total_items: number;
    items_learned: number;
    items_percentage: number;
    average_complexity: number;
  };
  milestones: {
    first_words: boolean;
    first_phrases: boolean;
    quarter_vocabulary: boolean;
    half_vocabulary: boolean;
    nearly_done: boolean;
  };
}

const endpoint = config.api.endpoints.progress;

export const progressApi = {
  /**
   * Get progress snapshot
   */
  getSnapshot: async (): Promise<ProgressSnapshot> => {
    return apiClient.get(`${endpoint}/snapshot`);
  },

  /**
   * Get detailed progress report
   */
  getDetailed: async (): Promise<DetailedProgress> => {
    return apiClient.get(`${endpoint}/detailed`);
  }
};

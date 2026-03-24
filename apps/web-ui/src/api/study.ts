/**
 * Study API endpoints
 */

import { apiClient } from './client';
import { config } from '@/config';

export interface StudyTarget {
  target_id: string;
  target_type: 'word' | 'phrase';
  target_value: string;
  target_translation: string;
  urgency_score: number;
  reason: string;
  audio_url?: string;
}

export interface StudyFeedback {
  target_id: string;
  correct: boolean;
  confidence: number;  // 1-5
  time_spent_seconds: number;
}

export interface FeedbackResponse {
  status: string;
  message: string;
  next_batch: StudyTarget[];
}

const endpoint = config.api.endpoints.study;

export const studyApi = {
  /**
   * Get next recommended items to study
   */
  getNextTargets: async (batchSize: number = 5): Promise<StudyTarget[]> => {
    return apiClient.get(`${endpoint}/next`, { batch_size: batchSize });
  },

  /**
   * Submit feedback on a studied item
   */
  submitFeedback: async (feedback: StudyFeedback): Promise<FeedbackResponse> => {
    return apiClient.post(`${endpoint}/feedback`, feedback);
  },

  /**
   * Get a full lesson plan
   */
  getLesson: async (lessonSize: number = 10): Promise<StudyTarget[]> => {
    return apiClient.get(`${endpoint}/lesson`, { lesson_size: lessonSize });
  }
};

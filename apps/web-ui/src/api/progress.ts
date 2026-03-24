/**/**






























































};  }    return apiClient.get(`${endpoint}/detailed`);  getDetailed: async (): Promise<DetailedProgress> => {   */   * Get detailed progress report  /**  },    return apiClient.get(`${endpoint}/snapshot`);  getSnapshot: async (): Promise<ProgressSnapshot> => {   */   * Get progress snapshot  /**export const progressApi = {const endpoint = config.api.endpoints.progress;}  };    nearly_done: boolean;    half_vocabulary: boolean;    quarter_vocabulary: boolean;    first_phrases: boolean;    first_words: boolean;  milestones: {  };    average_complexity: number;    items_percentage: number;    items_learned: number;    total_items: number;  overall: {  };    phrases_remaining: number;    phrases_percentage: number;    phrases_learned: number;    total_phrases: number;  phrases: {  };    words_remaining: number;    words_percentage: number;    words_learned: number;    total_words: number;  vocabulary: {export interface DetailedProgress {}  last_session_time?: string;  session_count: number;  average_complexity: number;  phrases_learned: number;  total_phrases: number;  words_learned: number;  total_words: number;export interface ProgressSnapshot {import { config } from '@/config';import { apiClient } from './client'; */ * Progress API endpoints * Audio API endpoints
 */

import { apiClient } from './client';
import { config } from '@/config';

const endpoint = config.api.endpoints.audio;

export const audioApi = {
  /**
   * Get audio file URL
   */
  getAudioUrl: (filename: string): string => {
    return `${endpoint}/${encodeURIComponent(filename)}`;
  },

  /**
   * List all available audio files
   */
  listAudioFiles: async (limit: number = 100) => {
    return apiClient.get<any>(`${endpoint}`, { limit });
  },

  /**
   * Get audio library statistics
   */
  getAudioStats: async () => {
    return apiClient.get<any>(`${endpoint}/stats`);
  }
};

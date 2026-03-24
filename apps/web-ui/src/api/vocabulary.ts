/**
 * Vocabulary API endpoints
 */

import { apiClient } from './client';
import { config } from '@/config';

export interface Word {
  value: string;
  translation: string;
  complexity: number;
  frequency: number;
  age: number;
}

export interface Phrase {
  value: string;
  translation: string;
  complexity: number;
  frequency: number;
  age: number;
  words: string[];
  dependencies: string[];
}

export interface VocabularyStats {
  id: string;
  value: string;
  item_type: 'word' | 'phrase';
  frequency: number;
  age: number;
  complexity: number;
  last_studied?: string;
}

export interface ProgressStats {
  total_words: number;
  words_learned: number;
  words_learned_percentage: number;
  total_phrases: number;
  phrases_learned: number;
  phrases_learned_percentage: number;
  average_complexity: number;
  total_items: number;
  items_learned: number;
}

const endpoint = config.api.endpoints.vocabulary;

export const vocabularyApi = {
  /**
   * Get all words with optional pagination and search
   */
  getWords: async (page?: number, pageSize: number = 20, search?: string) => {
    const params: any = { page_size: pageSize };
    if (page) params.page = page;
    if (search) params.search = search;
    return apiClient.get<any>(`${endpoint}/words`, params);
  },

  /**
   * Get a specific word
   */
  getWord: async (value: string): Promise<Word> => {
    return apiClient.get(`${endpoint}/words/${encodeURIComponent(value)}`);
  },

  /**
   * Get word statistics
   */
  getWordStats: async (value: string): Promise<VocabularyStats> => {
    return apiClient.get(`${endpoint}/words/${encodeURIComponent(value)}/stats`);
  },

  /**
   * Get all phrases with optional pagination and search
   */
  getPhrases: async (page?: number, pageSize: number = 20, search?: string) => {
    const params: any = { page_size: pageSize };
    if (page) params.page = page;
    if (search) params.search = search;
    return apiClient.get<any>(`${endpoint}/phrases`, params);
  },

  /**
   * Get a specific phrase
   */
  getPhrase: async (value: string): Promise<Phrase> => {
    return apiClient.get(`${endpoint}/phrases/${encodeURIComponent(value)}`);
  },

  /**
   * Get phrase statistics
   */
  getPhraseStats: async (value: string): Promise<VocabularyStats> => {
    return apiClient.get(`${endpoint}/phrases/${encodeURIComponent(value)}/stats`);
  },

  /**
   * Get overall progress snapshot
   */
  getProgress: async (): Promise<ProgressStats> => {
    return apiClient.get(`${endpoint}/progress`);
  }
};

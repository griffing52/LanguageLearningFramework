/**
 * Platform API endpoints
 */

import { apiClient } from './client';
import { config } from '@/config';

export interface PlatformStatus {
  counts: {
    words: number;
    phrases: number;
    lessons: number;
    tts_providers: number;
  };
  paths: {
    words_file: string;
    phrases_file: string;
    lessons_catalog_file: string;
    tts_providers_file: string;
    audio_dir: string;
  };
  tts_default_provider?: string;
}

export interface LessonEntry {
  item_type: 'word' | 'phrase';
  value: string;
}

export interface LessonDefinition {
  lesson_id: string;
  name: string;
  description?: string;
  items: LessonEntry[];
}

export interface TtsProviderConfig {
  provider_id: string;
  name: string;
  base_url: string;
  synthesize_path: string;
  health_path: string;
  api_key?: string;
  enabled: boolean;
  extra_headers: Record<string, string>;
}

const endpoint = config.api.endpoints.platform;

export const platformApi = {
  getStatus: async (): Promise<PlatformStatus> => {
    return apiClient.get(`${endpoint}/status`);
  },

  addWord: async (payload: {
    value: string;
    translation: string;
    complexity: number;
    frequency: number;
    age: number;
  }) => {
    return apiClient.post(`${endpoint}/words`, payload);
  },

  addPhrase: async (payload: {
    value: string;
    translation: string;
    complexity: number;
    frequency: number;
    age: number;
  }) => {
    return apiClient.post(`${endpoint}/phrases`, payload);
  },

  listLessons: async (): Promise<LessonDefinition[]> => {
    return apiClient.get(`${endpoint}/lessons`);
  },

  createLesson: async (payload: LessonDefinition) => {
    return apiClient.post(`${endpoint}/lessons`, payload);
  },

  listTtsProviders: async (): Promise<{ default_provider?: string; providers: TtsProviderConfig[] }> => {
    return apiClient.get(`${endpoint}/tts/providers`);
  },

  upsertTtsProvider: async (payload: TtsProviderConfig) => {
    return apiClient.post(`${endpoint}/tts/providers`, payload);
  },

  setDefaultProvider: async (providerId: string) => {
    return apiClient.post(`${endpoint}/tts/providers/${encodeURIComponent(providerId)}/default`);
  },

  runTtsInference: async (payload: {
    provider_id: string;
    text: string;
    language?: string;
    voice?: string;
    options?: Record<string, unknown>;
  }) => {
    return apiClient.post(`${endpoint}/tts/infer`, payload);
  }
};

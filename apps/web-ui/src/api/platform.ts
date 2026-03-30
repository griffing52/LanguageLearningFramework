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
    memory_entries: number;
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

export interface ImportResult {
  kind: 'words' | 'phrases' | 'memory';
  mode: 'replace' | 'append';
  imported_entries: number;
  target_file: string;
  total_after_import: number;
}

export interface TeachingSummary {
  total_words: number;
  total_phrases: number;
  taught_words: number;
  taught_phrases: number;
  total_word_frequency: number;
  total_phrase_frequency: number;
  total_taught_frequency: number;
}

export interface TeachingItem {
  value: string;
  translation: string;
  frequency: number;
  complexity: number;
  age: number;
}

export interface TeachingStatistics {
  summary: TeachingSummary;
  top_words: TeachingItem[];
  top_phrases: TeachingItem[];
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
  },

  importWords: async (file: File, mode: 'replace' | 'append' = 'replace'): Promise<{ status: string; result: ImportResult }> => {
    const form = new FormData();
    form.append('file', file);
    form.append('mode', mode);
    return apiClient.postForm(`${endpoint}/import/words`, form);
  },

  importPhrases: async (file: File, mode: 'replace' | 'append' = 'replace'): Promise<{ status: string; result: ImportResult }> => {
    const form = new FormData();
    form.append('file', file);
    form.append('mode', mode);
    return apiClient.postForm(`${endpoint}/import/phrases`, form);
  },

  importMemory: async (file: File, mode: 'replace' | 'append' = 'replace'): Promise<{ status: string; result: ImportResult }> => {
    const form = new FormData();
    form.append('file', file);
    form.append('mode', mode);
    return apiClient.postForm(`${endpoint}/import/memory`, form);
  },

  saveMemoryState: async (exportFileName?: string): Promise<{ status: string; result: { entries: number; saved_file: string; export_file?: string } }> => {
    const suffix = exportFileName ? `?export_file_name=${encodeURIComponent(exportFileName)}` : '';
    return apiClient.post(`${endpoint}/memory/save${suffix}`);
  },

  clearDataset: async (target: 'words' | 'phrases' | 'memory' | 'all') => {
    return apiClient.post(`${endpoint}/clear?target=${encodeURIComponent(target)}`);
  },

  getTeachingStatistics: async (topN: number = 10): Promise<TeachingStatistics> => {
    return apiClient.get(`${endpoint}/statistics`, { top_n: topN });
  }
};

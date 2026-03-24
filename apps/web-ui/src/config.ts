/**
 * Environment configuration
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';

export const config = {
  api: {
    baseUrl: API_BASE_URL,
    endpoints: {
      vocabulary: `${API_BASE_URL}/vocabulary`,
      study: `${API_BASE_URL}/study`,
      audio: `${API_BASE_URL}/audio`,
      progress: `${API_BASE_URL}/progress`,
    }
  },
  study: {
    defaultBatchSize: 5,
    defaultLessonSize: 10,
  }
};

export default config;

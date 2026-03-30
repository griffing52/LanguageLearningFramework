/**
 * API Client
 * 
 * Single point of contact for all backend communication.
 * Encapsulates HTTP requests, error handling, and response transformation.
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { config } from '@/config';

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages?: number;
}

class ApiClient {
  private client: AxiosInstance;

  constructor(baseUrl: string) {
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      response => response,
      error => this.handleError(error)
    );
  }

  private handleError(error: AxiosError) {
    if (error.response) {
      // Server responded with error status
      console.error(`API Error [${error.response.status}]:`, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('No response from API:', error.message);
    } else {
      console.error('API Error:', error.message);
    }
    return Promise.reject(error);
  }

  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const response = await this.client.get<T>(endpoint, { params });
    return response.data;
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    const response = await this.client.post<T>(endpoint, data);
    return response.data;
  }

  async postForm<T>(endpoint: string, data: FormData): Promise<T> {
    const response = await this.client.post<T>(endpoint, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    const response = await this.client.put<T>(endpoint, data);
    return response.data;
  }

  async delete<T>(endpoint: string): Promise<T> {
    const response = await this.client.delete<T>(endpoint);
    return response.data;
  }
}

export const apiClient = new ApiClient(config.api.baseUrl);

/**
 * Error handling utilities
 * Converts raw API errors into user-friendly messages
 */

import { AxiosError } from 'axios';

interface ErrorContext {
  endpoint?: string;
  action?: string;
}

/**
 * Convert API errors to user-friendly messages
 */
export function getUserFriendlyError(error: unknown, _context?: ErrorContext): string {
  // Handle Axios errors
  if (error instanceof AxiosError) {
    // Specific status code handling
    switch (error.response?.status) {
      case 400:
        return `The request had invalid data. Please check and try again.`;
      case 404:
        return `The resource wasn't found. It may have been deleted.`;
      case 422:
        // Validation error - try to extract more detail
        const data = error.response?.data as any;
        if (data?.detail) {
          return `Please check your input: ${data.detail}`;
        }
        return `The data you provided isn't valid. Please review and try again.`;
      case 500:
      case 502:
      case 503:
        return `The server is experiencing issues. Please try again in a moment.`;
      case 429:
        return `You're requesting too frequently. Please wait a moment and try again.`;
      case 401:
        return `You need to log in to continue.`;
      case 403:
        return `You don't have permission to perform this action.`;
      default:
        // Generic network error
        if (!error.response) {
          return `Connection problem. Please check your internet and try again.`;
        }
        return `Something went wrong. Please try again.`;
    }
  }

  // Handle standard Error objects
  if (error instanceof Error) {
    // Check for common error messages and make them friendly
    const msg = error.message.toLowerCase();
    
    if (msg.includes('timeout')) {
      return `The request took too long. Please try again.`;
    }
    if (msg.includes('network')) {
      return `Network connection problem. Please check your internet.`;
    }
    
    // Return original message if it's already user-friendly
    return error.message;
  }

  // Fallback
  return `An unexpected error occurred. Please try again.`;
}

/**
 * Get error details for debugging (logged to console)
 */
export function logErrorDetails(error: unknown, context?: ErrorContext): void {
  console.error('Error Details:', {
    context,
    error,
    timestamp: new Date().toISOString()
  });
}

/**
 * Check if error is retriable
 */
export function isRetriableError(error: unknown): boolean {
  if (error instanceof AxiosError) {
    const status = error.response?.status;
    // Retry on 429, 503, 504, and network errors
    return status === 429 || status === 503 || status === 504 || !error.response;
  }
  return false;
}

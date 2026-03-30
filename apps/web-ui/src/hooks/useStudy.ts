/**
 * Custom hook for study session management
 */

import { useState, useCallback, useEffect } from 'react';
import { StudyTarget } from '@/api/study';
import { studyService } from '@/services/studyService';
import { getUserFriendlyError } from '@/utils/errorHandler';

export interface StudyState {
  targets: StudyTarget[];
  currentIndex: number;
  isLoading: boolean;
  error: string | null;
}

export function useStudy(lessonSize: number = 10) {
  const [state, setState] = useState<StudyState>({
    targets: [],
    currentIndex: 0,
    isLoading: false,
    error: null
  });

  // Load lesson on mount
  useEffect(() => {
    const loadLesson = async () => {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      try {
        await studyService.loadLesson(lessonSize);
        const current = studyService.getCurrentTarget();
        setState(prev => ({
          ...prev,
          targets: [current!],
          isLoading: false
        }));
      } catch (error) {
        setState(prev => ({
          ...prev,
          error: getUserFriendlyError(error),
          isLoading: false
        }));
      }
    };

    loadLesson();
  }, [lessonSize]);

  const getCurrentTarget = useCallback(() => {
    return studyService.getCurrentTarget();
  }, []);

  const moveNext = useCallback(async () => {
    const hasNext = studyService.nextTarget();
    const nextTarget = studyService.getCurrentTarget();
    
    if (hasNext && nextTarget) {
      setState(prev => ({
        ...prev,
        currentIndex: prev.currentIndex + 1,
        targets: [nextTarget]
      }));
    }
    
    return hasNext;
  }, []);

  const submitFeedback = useCallback(async (correct: boolean, confidence: number, timeSpent: number) => {
    try {
      await studyService.submitFeedback({
        correct,
        confidence,
        time_spent_seconds: timeSpent
      });
      setState(prev => ({ ...prev, error: null }));
      return true;
    } catch (error) {
      const message = getUserFriendlyError(error);
      setState(prev => ({
        ...prev,
        error: message
      }));
      return false;
    }
  }, []);

  return {
    getCurrentTarget,
    moveNext,
    submitFeedback,
    progress: studyService.getProgress(),
    isLoading: state.isLoading,
    error: state.error,
    isComplete: studyService.isLessonComplete()
  };
}

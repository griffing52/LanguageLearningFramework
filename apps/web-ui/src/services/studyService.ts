/**
 * Study service - frontend business logic
 */

import { studyApi, StudyTarget, StudyFeedback } from '@/api/study';

export class StudyService {
  private currentLesson: StudyTarget[] = [];
  private currentIndex = 0;

  /**
   * Load a lesson plan
   */
  async loadLesson(lessonSize: number = 10): Promise<void> {
    this.currentLesson = await studyApi.getLesson(lessonSize);
    this.currentIndex = 0;
  }

  /**
   * Load next batch of study targets
   */
  async loadNextBatch(batchSize: number = 5): Promise<StudyTarget[]> {
    return studyApi.getNextTargets(batchSize);
  }

  /**
   * Get current study target
   */
  getCurrentTarget(): StudyTarget | null {
    if (this.currentIndex < this.currentLesson.length) {
      return this.currentLesson[this.currentIndex];
    }
    return null;
  }

  /**
   * Move to next target
   */
  nextTarget(): boolean {
    if (this.currentIndex < this.currentLesson.length - 1) {
      this.currentIndex++;
      return true;
    }
    return false;
  }

  /**
   * Submit feedback for current target
   */
  async submitFeedback(feedback: Omit<StudyFeedback, 'target_id'>): Promise<void> {
    const target = this.getCurrentTarget();
    if (!target) throw new Error('No current target');

    const fullFeedback: StudyFeedback = {
      target_id: target.target_id,
      ...feedback
    };

    await studyApi.submitFeedback(fullFeedback);
  }

  /**
   * Get lesson progress
   */
  getProgress(): { current: number; total: number } {
    return {
      current: this.currentIndex + 1,
      total: this.currentLesson.length
    };
  }

  /**
   * Check if lesson is complete
   */
  isLessonComplete(): boolean {
    return this.currentIndex >= this.currentLesson.length - 1;
  }
}

export const studyService = new StudyService();

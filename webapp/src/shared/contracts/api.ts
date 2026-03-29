import { LessonPlan } from "@/src/modules/lesson-planner/domain/types";

export interface PlanLessonRequest {
  learnerId: string;
  languageCode: string;
  targetGoal: string;
  maxItems?: number;
}

export type PlanLessonResponse = LessonPlan;

export interface GenerateAudioRequest {
  lessonPlan: LessonPlan;
}

export type LanguageCode = string;

export interface LearnerSnapshot {
  learnerId: string;
  languageCode: LanguageCode;
  knownConceptIds: string[];
  recentFailures: string[];
}

export interface LessonCandidate {
  phraseId: string;
  phraseText: string;
  meaning: string;
  conceptIds: string[];
  difficulty: number;
}

export interface LessonItem {
  phraseId: string;
  phraseText: string;
  meaning: string;
  unknownConceptIds: string[];
  priorityScore: number;
}

export interface LessonPlan {
  planId: string;
  learnerId: string;
  languageCode: LanguageCode;
  targetGoal: string;
  items: LessonItem[];
  createdAtIso: string;
}

export interface PlanNextLessonInput {
  learnerId: string;
  languageCode: LanguageCode;
  targetGoal: string;
  maxItems?: number;
}

export interface LessonPlannerPort {
  planNextLesson(input: PlanNextLessonInput): Promise<LessonPlan>;
}

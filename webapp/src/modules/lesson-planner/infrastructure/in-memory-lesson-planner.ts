import {
  LessonCandidate,
  LessonPlan,
  LessonPlannerPort,
  PlanNextLessonInput,
} from "@/src/modules/lesson-planner/domain/types";

const CATALOG: Record<string, LessonCandidate[]> = {
  "gsw-CH": [
    {
      phraseId: "gsw-greeting-1",
      phraseText: "Hoi, wie gaht's?",
      meaning: "Hi, how are you?",
      conceptIds: ["greeting", "question-form", "gaht"],
      difficulty: 1,
    },
    {
      phraseId: "gsw-cafe-1",
      phraseText: "Ich ha gern en Kafi, bitte.",
      meaning: "I would like a coffee, please.",
      conceptIds: ["politeness", "food-drink", "ich-ha-gern"],
      difficulty: 2,
    },
    {
      phraseId: "gsw-train-1",
      phraseText: "Wo isch dr Bahnhof?",
      meaning: "Where is the train station?",
      conceptIds: ["location-query", "question-word-wo", "bahnhof"],
      difficulty: 2,
    },
    {
      phraseId: "gsw-help-1",
      phraseText: "Chasch mer bitte hälfe?",
      meaning: "Can you help me, please?",
      conceptIds: ["request-help", "modal-form", "politeness"],
      difficulty: 3,
    },
  ],
  en: [
    {
      phraseId: "en-greeting-1",
      phraseText: "Hi, how are you?",
      meaning: "Greeting and wellness check.",
      conceptIds: ["greeting", "question-form"],
      difficulty: 1,
    },
  ],
};

export class InMemoryLessonPlanner implements LessonPlannerPort {
  async planNextLesson(input: PlanNextLessonInput): Promise<LessonPlan> {
    const maxItems = input.maxItems ?? 3;
    const candidates = CATALOG[input.languageCode] ?? CATALOG.en;
    const ranked = candidates
      .map((candidate) => {
        const goalBoost = this.goalScore(candidate, input.targetGoal);

        return {
          ...candidate,
          priorityScore: goalBoost + 100 - candidate.difficulty * 10,
        };
      })
      .sort((a, b) => b.priorityScore - a.priorityScore)
      .slice(0, maxItems)
      .map((candidate) => ({
        phraseId: candidate.phraseId,
        phraseText: candidate.phraseText,
        meaning: candidate.meaning,
        unknownConceptIds: candidate.conceptIds,
        priorityScore: candidate.priorityScore,
      }));

    return {
      planId: crypto.randomUUID(),
      learnerId: input.learnerId,
      languageCode: input.languageCode,
      targetGoal: input.targetGoal,
      items: ranked,
      createdAtIso: new Date().toISOString(),
    };
  }

  private goalScore(candidate: LessonCandidate, targetGoal: string): number {
    const normalizedGoal = targetGoal.toLowerCase();
    const text = `${candidate.phraseText} ${candidate.meaning}`.toLowerCase();

    if (normalizedGoal.length === 0) {
      return 0;
    }

    return text.includes(normalizedGoal) ? 30 : 0;
  }
}

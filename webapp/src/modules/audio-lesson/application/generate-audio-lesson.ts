import {
  AudioLesson,
  NarrationSegment,
  SpeechSynthesisPort,
} from "@/src/modules/audio-lesson/domain/types";
import { LessonPlan } from "@/src/modules/lesson-planner/domain/types";

export class GenerateAudioLessonUseCase {
  constructor(private readonly synthesisPort: SpeechSynthesisPort) {}

  async execute(input: { lessonPlan: LessonPlan }): Promise<AudioLesson> {
    const segments = this.createNarrationSegments(input.lessonPlan);

    return this.synthesisPort.synthesizeLesson({
      lessonPlanId: input.lessonPlan.planId,
      languageCode: input.lessonPlan.languageCode,
      segments,
    });
  }

  private createNarrationSegments(lessonPlan: LessonPlan): NarrationSegment[] {
    const intro: NarrationSegment = {
      segmentId: `${lessonPlan.planId}-intro`,
      text: `Lesson goal: ${lessonPlan.targetGoal}.`,
    };

    const phraseSegments = lessonPlan.items.flatMap((item, index) => {
      const order = index + 1;
      const lineA: NarrationSegment = {
        segmentId: `${lessonPlan.planId}-${item.phraseId}-a`,
        text: `Phrase ${order}: ${item.phraseText}`,
      };
      const lineB: NarrationSegment = {
        segmentId: `${lessonPlan.planId}-${item.phraseId}-b`,
        text: `Meaning: ${item.meaning}`,
      };

      return [lineA, lineB];
    });

    const outro: NarrationSegment = {
      segmentId: `${lessonPlan.planId}-outro`,
      text: "End of lesson. Replay each phrase and practice out loud.",
    };

    return [intro, ...phraseSegments, outro];
  }
}

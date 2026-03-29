import { GenerateAudioLessonUseCase } from "@/src/modules/audio-lesson/application/generate-audio-lesson";
import { MockSpeechSynthesizer } from "@/src/modules/audio-lesson/infrastructure/mock-speech-synthesizer";
import { PlanNextLessonUseCase } from "@/src/modules/lesson-planner/application/plan-next-lesson";
import { InMemoryLessonPlanner } from "@/src/modules/lesson-planner/infrastructure/in-memory-lesson-planner";

const planner = new InMemoryLessonPlanner();
const speechSynthesizer = new MockSpeechSynthesizer();

export const useCases = {
  planNextLesson: new PlanNextLessonUseCase(planner),
  generateAudioLesson: new GenerateAudioLessonUseCase(speechSynthesizer),
};

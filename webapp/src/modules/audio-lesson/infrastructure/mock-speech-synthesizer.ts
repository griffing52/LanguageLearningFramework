import {
  AudioLesson,
  NarrationSegment,
  SpeechSynthesisPort,
} from "@/src/modules/audio-lesson/domain/types";

export class MockSpeechSynthesizer implements SpeechSynthesisPort {
  async synthesizeLesson(input: {
    lessonPlanId: string;
    languageCode: string;
    segments: NarrationSegment[];
  }): Promise<AudioLesson> {
    return {
      lessonAudioId: crypto.randomUUID(),
      lessonPlanId: input.lessonPlanId,
      provider: "mock-speech-synthesizer",
      languageCode: input.languageCode,
      streamUrl: `/api/audio/mock-stream/${input.lessonPlanId}`,
      transcript: input.segments,
      createdAtIso: new Date().toISOString(),
    };
  }
}

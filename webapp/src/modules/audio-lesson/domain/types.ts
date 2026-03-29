export interface NarrationSegment {
  segmentId: string;
  text: string;
  voiceHint?: string;
}

export interface AudioLesson {
  lessonAudioId: string;
  lessonPlanId: string;
  provider: string;
  languageCode: string;
  streamUrl: string;
  transcript: NarrationSegment[];
  createdAtIso: string;
}

export interface SpeechSynthesisPort {
  synthesizeLesson(input: {
    lessonPlanId: string;
    languageCode: string;
    segments: NarrationSegment[];
  }): Promise<AudioLesson>;
}

# Architecture Overview

This repository now follows a modular structure intended for long-term scalability across multiple target languages.

## Design Principles

- Domain first: planning and audio generation logic is represented by stable interfaces.
- Implementation hiding: UI and routes do not know concrete planner or TTS provider details.
- Composition root: infrastructure adapters are bound once in server composition.
- Language agnostic core: language-specific data is isolated in catalogs and future language packs.

## Current Modules

- lesson-planner
  - Domain contracts for lesson planning.
  - In-memory planner implementation for initial development.
  - Use case wrapper for application orchestration.
- audio-lesson
  - Domain contracts for narration and synthesis.
  - Mock speech synthesizer adapter.
  - Use case to convert lesson plans into narration segments.
- lesson-workbench
  - Client UI to create plans and trigger audio generation.

## Composition Root

- src/server/composition.ts binds:
  - PlanNextLessonUseCase -> InMemoryLessonPlanner
  - GenerateAudioLessonUseCase -> MockSpeechSynthesizer

Swap implementations there without changing route handlers or UI.

## API Surface

- POST /api/lessons/plan
  - Input: learnerId, languageCode, targetGoal, maxItems
  - Output: lesson plan with ranked items
- POST /api/audio/generate
  - Input: lessonPlan
  - Output: audio lesson metadata and transcript segments
- GET /api/audio/mock-stream/[planId]
  - Placeholder stream endpoint for mock provider

## Next Professionalization Steps

1. Add persistence adapters (PostgreSQL recommended):
   - learner profiles
   - concept graph
   - lesson history
   - generated audio metadata
2. Replace mock TTS with provider adapter and robust retries.
3. Add background job queue for synthesis tasks.
4. Add contract tests for planner and TTS ports.
5. Add language-pack module with tokenizer and morphology strategies per language.

## Decision Log Needed

The following decisions are required before production implementation:

1. Primary data store and hosting model.
2. TTS provider preference and acceptable cost/latency profile.
3. Audio format and retention policy.
4. Whether lesson synthesis should be synchronous or queued.
5. Authentication approach and tenant model.

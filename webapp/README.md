# Language Learning Framework Web App

Adaptive phrase-first lesson planning with modular audio lesson generation.

## Current Vertical Slice

- Plan lessons from a target goal using a language-aware phrase catalog.
- Generate narration segments from lesson plans.
- Trigger mock audio generation endpoint.
- Play transcript with browser speech synthesis.

## Architecture

See ARCHITECTURE.md for module boundaries, composition strategy, and production decisions.

## Development Commands

Install dependencies:

npm install

Run local development server:

npm run dev

Run lint:

npm run lint

## API Endpoints

- POST /api/lessons/plan
- POST /api/audio/generate
- GET /api/audio/mock-stream/[planId]

## Current Caveats

- Planner uses in-memory demo catalog.
- Audio provider is mock-only and does not synthesize real waveform files.
- No persistent learner state yet.

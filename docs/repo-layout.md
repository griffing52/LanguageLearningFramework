# Repository Layout

This repository now follows a component-oriented structure so it can grow beyond a single C++ executable.

## Top-level folders

- `apps/`
  - Runtime applications.
  - `apps/cpp-cli/` contains current C++ source and headers.
  - `apps/web-ui/` is reserved for the upcoming browser interface.
- `data/`
  - Shared and local data files used by runtime components.
  - `data/seed/` contains baseline dictionaries and lesson files.
  - `data/state/` contains mutable local runtime state.
  - `data/audio/` contains generated or source audio assets.
- `tools/`
  - Non-runtime helper scripts.
  - `tools/scraping/` for content collection/cleanup.
  - `tools/tts/` for speech generation and audio processing.
- `docs/`
  - MkDocs content for architecture, usage, and development references.

## Why this layout

- Separates runtime apps from tooling scripts.
- Keeps mutable data distinct from source code.
- Creates a clear place for the future web UI.
- Supports introducing a local C++ service layer without reshuffling the repo again.

## Current compatibility choices

- `LanguageLearningFramework.sln` and `LanguageLearningFramework.vcxproj` remain at repository root for minimal workflow disruption.
- C++ source files moved under `apps/cpp-cli/` and are referenced from the project file.
- CLI defaults now point to `data/seed/words.txt` and `data/state/mem0`.

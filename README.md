# LanguageLearningFramework

LanguageLearningFramework is a local, file-based language study project with:

- A C++ interactive CLI for word and phrase memory management.
- Scraping helpers for collecting lesson content.
- Text-to-speech helper scripts for generating lesson audio.
- A planned web UI that will interact with a local C++ service.

## Project structure

- `apps/cpp-cli/`: C++ source and headers.
- `apps/web-ui/`: reserved for the future browser UI.
- `data/seed/`: baseline dictionaries and lesson files.
- `data/state/`: local runtime state such as `mem0`.
- `data/audio/`: generated and source audio assets.
- `tools/scraping/`: scraping scripts and source lists.
- `tools/tts/`: TTS generation and audio assembly scripts.
- `docs/` and `mkdocs.yml`: documentation site.

Visual Studio solution and project files are currently kept at repository root to avoid breaking existing local workflows.

## Building the C++ solution

1. Open LanguageLearningFramework.sln in Visual Studio.
2. Build in Debug or Release.
3. Run the generated executable.

## Documentation with MkDocs

This repository now includes a full MkDocs documentation site.

Install docs dependencies:

```powershell
pip install -r requirements-docs.txt
```

Preview docs locally:

```powershell
mkdocs serve
```

Build static docs:

```powershell
mkdocs build
```

### Docs entry points

- docs/index.md
- docs/getting-started.md
- docs/cli-reference.md
- docs/data-files.md
- docs/architecture.md
- docs/tooling.md
- docs/tts-methods/index.md
- docs/development.md
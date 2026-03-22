# LanguageLearningFramework

LanguageLearningFramework is a local, file-based language study project with:

- A C++ interactive CLI for word and phrase memory management.
- Scraping helpers for collecting lesson content.
- Text-to-speech helper scripts for generating lesson audio.

## Project structure

- C++ core: root-level .cpp/.h files and Visual Studio solution files.
- Scraping scripts: scraping/.
- TTS scripts: tts/.
- Documentation site: docs/ and mkdocs.yml.

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
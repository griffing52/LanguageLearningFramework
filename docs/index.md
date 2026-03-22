# Language Learning Framework

LanguageLearningFramework is a local, file-driven language study toolkit focused on phrase learning.

!!! info "What this project is"
    A C++ study engine with helper scripts for scraping and TTS, designed around plain-text data files for easy iteration.

The repository currently includes:

- A C++ interactive CLI for loading words and phrase memory, inspecting dependencies, and adjusting metadata.
- A scraping helper for collecting Swiss German lesson content.
- Text-to-speech helper scripts for generating and composing audio assets.

## At a glance

| Area | Stack | Purpose |
| --- | --- | --- |
| Core app | C++ | Interactive prompt for word and phrase study data |
| Scraping tools | JavaScript + Python | Collect and clean lesson source content |
| Audio tools | Python | Generate and stitch spoken lesson assets |
| Documentation | MkDocs | Project reference and onboarding |

## Quick start

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

## Documentation map

- Use [Getting Started](getting-started.md) to set up build tools and run the app.
- Use [CLI Reference](cli-reference.md) for commands supported by the interactive prompt.
- Use [Data Files](data-files.md) to understand input file formats.
- Use [Architecture](architecture.md) for module responsibilities and data flow.
- Use [Tooling](tooling.md) for scraping and TTS helpers.
- Use [TTS Methods](tts-methods/index.md) for approach history, tradeoffs, and current direction.
- Use [Development Notes](development.md) for extension guidance.

## Current project status

The core CLI supports loading, inspection, memory save/load, and selected metadata updates. Several commands are placeholders and are documented as such.

!!! warning "Implementation status"
    Parser branches for add, remove, and list are currently placeholders in the CLI.

# Language Learning Framework

LanguageLearningFramework is a comprehensive language learning system combining a modern web UI, REST API backend, spaced repetition algorithm, and C++ data toolkit—all powered by local file-based architecture.

## What's Included

### Web Application Stack
- **React UI** - Interactive study interface with audio playback, confidence feedback, and progress tracking
- **FastAPI Backend** - Professional 5-layer REST API with spaced repetition algorithm
- **Docker Orchestration** - Complete containerized stack (UI, API, data initialization)

### Legacy C++ Toolkit
- **CLI Application** - Interactive prompt for direct word/phrase data management
- **Scraping Tools** - Swiss German lesson content collection and cleaning
- **TTS System** - Audio generation and composition pipeline

## Technology Stack

| Component | Technology | Purpose |
| --- | --- | --- |
| Frontend | React 18 + TypeScript + Vite | Interactive study UI |
| Backend | FastAPI + Pydantic + Uvicorn | REST API with spaced repetition |
| Container | Docker + Nginx | Full-stack deployment |
| C++ Legacy | C++ + CMake | CLI data tool |
| Scraping | JavaScript + Python | Content acquisition |
| Audio | Python (SpeechT5, Concatenative) | TTS generation |
| Docs | MkDocs + Material | Documentation |

## Quick Start

Get everything running in 5 minutes:

```bash
# Windows
.\start-dev.ps1

# macOS/Linux
./start-dev.sh
```

Then open:
- **UI**: http://localhost:3000
- **API**: http://127.0.0.1:5000
- **API Docs**: http://127.0.0.1:5000/api/docs

## Documentation Map

**Getting Started** — Use [Quick Start](quick-start.md) to run the web stack in 5 minutes, then [Setup](setup.md) for detailed configuration and development guidance.

**Web Stack** — Explore [Backend Architecture](backend/overview.md) for API design, [Frontend Architecture](frontend/overview.md) for React components, and [API Reference](api/reference.md) for all endpoints.

**Deployment** — See [Docker & Deployment](deployment/docker.md) for containerization, Kubernetes, and production hosting options. For split-machine inference, use [Remote TTS Server](deployment/remote-tts-server.md).

**Repository & Legacy** — Use [Repository Layout](repo-layout.md) for project structure, [CLI Reference](cli-reference.md) for C++ commands, and [Data Files](data-files.md) for file formats.

**Extended Reading** — Advanced topics: [Architecture](architecture.md), [Tooling](tooling.md), [TTS Methods](tts-methods/index.md), [Development Notes](development.md).

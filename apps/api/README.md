# Language Learning Framework API

Modular FastAPI backend serving the Language Learning Framework.

## Architecture

### Layers

- **API Layer** (`api/`): FastAPI route handlers, request/response marshalling
- **Service Layer** (`services/`): Business logic (study planning, vocabulary operations, audio management)
- **Data Access Layer** (`data_access/`): Repository pattern, file loading, in-memory caching
- **Core** (`core/`): Domain models (Pydantic DTOs) and constants
- **Utils** (`utils/`): Logging, file path management, and other utilities

### Design Principles

- **Information Hiding**: Each layer exposes only necessary interfaces
- **Separation of Concerns**: Routes handle HTTP, services handle logic, data_access handles files
- **Repository Pattern**: Clean abstraction over data sources
- **Type Safety**: Pydantic models for all inputs/outputs
- **Dependency Injection**: Services are initialized with repository access

## Quick Start

### Prerequisites

- Python 3.9+
- Poetry or pip

### Installation

```bash
cd apps/api

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy the `.env.example` to `.env` and adjust settings:

```bash
API_HOST=127.0.0.1
API_PORT=5000
API_DEBUG=False
API_RELOAD=True
CORS_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO
```

### Running the Server

```bash
python app.py
```

Or with uvicorn directly:

```bash
uvicorn app:app --host 127.0.0.1 --port 5000 --reload
```

The API will be available at `http://localhost:5000`

- Interactive docs: `http://localhost:5000/api/docs`
- ReDoc: `http://localhost:5000/api/redoc`
- OpenAPI JSON: `http://localhost:5000/api/openapi.json`

## API Endpoints

### Vocabulary

- `GET /api/vocabulary/words` - List all words (paginated)
- `GET /api/vocabulary/words/{value}` - Get specific word
- `GET /api/vocabulary/words/{value}/stats` - Get word statistics
- `GET /api/vocabulary/phrases` - List all phrases (paginated)
- `GET /api/vocabulary/phrases/{value}` - Get specific phrase
- `GET /api/vocabulary/phrases/{value}/stats` - Get phrase statistics
- `GET /api/vocabulary/progress` - Overall progress snapshot

### Study Sessions

- `GET /api/study/next` - Get next items to study (spaced repetition)
- `POST /api/study/feedback` - Submit study feedback and get next item
- `GET /api/study/lesson` - Get full lesson plan

### Audio

- `GET /api/audio/{filename}` - Serve audio file
- `GET /api/audio` - List available audio files
- `GET /api/audio/stats` - Get audio library statistics

### Progress

- `GET /api/progress/snapshot` - Current progress snapshot
- `GET /api/progress/detailed` - Detailed progress with breakdowns

### Platform Manager (CLI parity + UI operations)

- `GET /api/platform/status` - Platform status and file path summary
- `POST /api/platform/words` - Create one word entry
- `POST /api/platform/phrases` - Create one phrase entry
- `GET /api/platform/lessons` - List user-defined lessons
- `POST /api/platform/lessons` - Create a lesson from words/phrases
- `POST /api/platform/import/words` - Upload full word list file (`multipart/form-data`)
- `POST /api/platform/import/phrases` - Upload full phrase list file (`multipart/form-data`)
- `POST /api/platform/import/memory` - Upload memory file (`.json` or `value|frequency` lines)
- `POST /api/platform/memory/save` - Persist in-memory state (optional `export_file_name` query)
- `POST /api/platform/clear?target=words|phrases|memory|all` - Clear selected datasets
- `GET /api/platform/statistics` - Aggregate taught counts and top taught words/phrases
- `GET /api/platform/tts/providers` - List configured TTS providers
- `POST /api/platform/tts/providers` - Upsert a TTS provider
- `POST /api/platform/tts/providers/{provider_id}/default` - Set default TTS provider
- `POST /api/platform/tts/infer` - Run provider inference request

## Data Flow

```
C++ seed data (words.txt, lesson1.txt)
          ↓
    DataLoader (parser)
          ↓
    Repository (cache + in-memory store)
          ↓
    Services (business logic)
          ↓
    API Routes (HTTP endpoints)
          ↓
    React Frontend
```

## Services

### VocabularyService
Handles vocabulary operations: word/phrase retrieval, search, statistics

### StudyService
Core spaced repetition algorithm, study recommendation, feedback recording

### AudioService
Audio file management and serving

### ProgressService
Learning progress tracking and reporting

### PlatformService
Unified platform operations for CRUD, uploads/imports, lesson planning, memory save/export, clear actions, teaching statistics, and TTS provider orchestration.

## UI-first Workflow

The UI now supports core CLI-equivalent operations through the platform routes:

1. Upload/replace or append your `words`, `phrases`, and `memory` files
2. Create or update vocabulary and lessons from forms
3. Save current memory state to default `mem0` (and optional export file)
4. View teaching statistics (total taught events and top words/phrases)
5. Manage TTS from a dedicated UI page separate from data management

## Development

### Adding a New Endpoint

1. Create service method in `services/`
2. Add Pydantic model in `core/models.py` if needed
3. Create route handler in `api/`
4. Include router in `app.py`

### Testing

TODO: Add pytest fixtures and tests

### Memory Persistence

Study progress is saved to `data/state/mem0` (JSON format) and reloaded on startup.


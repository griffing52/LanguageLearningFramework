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


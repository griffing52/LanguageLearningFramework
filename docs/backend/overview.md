# Backend Architecture

Professional Python backend with FastAPI and clean layered architecture.

## Architecture Layers

The backend follows a 5-layer architecture for maximum modularity and maintainability:

```
┌─────────────────────────────────────┐
│      API Routes (FastAPI)           │  Route handlers, HTTP I/O
│      (api/*.py)                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Service Layer                  │  Business logic, algorithms
│      (services/*.py)                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Data Access Layer              │  Repository pattern
│      (data_access/*.py)             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Core Domain Models             │  Pydantic DTOs, constants
│      (core/*.py)                    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Utilities                      │  Logging, paths, helpers
│      (utils/*.py)                   │
└─────────────────────────────────────┘
```

## Module Responsibilities

### API Layer (`api/`)

REST endpoints for HTTP clients.

| Module | Endpoints | Responsibility |
|--------|-----------|-----------------|
| `vocabulary.py` | `/vocabulary/*` | Word/phrase operations |
| `study.py` | `/study/*` | Study sessions & feedback |
| `audio.py` | `/audio/*` | Audio file serving |
| `progress.py` | `/progress/*` | Learning statistics |

**Key Principle**: Routes marshal HTTP requests/responses. Business logic delegated to services.

### Service Layer (`services/`)

Business logic and algorithms.

| Service | Responsibility |
|---------|-----------------|
| `vocabulary_service.py` | Vocabulary operations, search, statistics |
| `study_service.py` | Spaced repetition algorithm, study planning |
| `audio_service.py` | Audio file management and listing |
| `progress_service.py` | Progress tracking and reporting |

**Key Principle**: Pure business logic, independent of HTTP/database specifics.

### Data Access Layer (`data_access/`)

Repository pattern for data access.

| Module | Responsibility |
|--------|-----------------|
| `loader.py` | File parsing and data deserialization |
| `repository.py` | In-memory cache, lazy loading, data persistence |

**Key Principle**: Single abstraction for all data access. Easy to swap implementations.

### Core (`core/`)

Domain models and constants.

| Module | Contents |
|--------|----------|
| `models.py` | Pydantic DTOs with validation |
| `constants.py` | Enums, thresholds, default values |

**Key Principle**: Single source of truth for data contracts.

### Utilities (`utils/`)

Helper functions and shared utilities.

| Module | Responsibility |
|--------|-----------------|
| `file_paths.py` | Centralized path management |
| `logger.py` | Structured logging configuration |

## Data Flow

```
Request from Frontend (React)
         ↓
    Route Handler (api/*.py)
         ↓
    Service Layer (services/*.py)
         ↓
    Repository (data_access/repository.py)
         ↓
    Data Loader (data_access/loader.py)
         ↓
    File System (data/seed/, data/state/, data/audio/)
         ↓
    Response to Frontend
```

## Key Features

### Spaced Repetition Algorithm

Located in `services/study_service.py::_calculate_urgency_score()`.

**Scoring Logic:**
- Never-studied items get highest priority (frequency = 0)
- Items needing review boosted by age (sessions since study)
- Lower complexity gets slight preference
- Phrases prioritized over words
- Random shuffling within tiers for variety

**Formula:**
```
score = 100 (if frequency == 0)
      + frequency^-1               # Inverse: lower freq = higher score
      + age * 0.5 (if age > 50)    # Urgent if old
      + age * 0.1 (otherwise)      # Subtle boost for age
      + complexity_factor          # Simpler items preferred
      + 10 (for phrases)           # Phrase priority
```

### Type Safety

All API contracts defined with Pydantic models in `core/models.py`:
- Automatic validation on input
- Automatic serialization on output
- Clear documentation via schema
- IDE autocompletion support

### Lazy Loading & Caching

Repository pattern with intelligent caching:
- Data loaded on first access (lazy)
- Cached in memory for session
- Can easily swap to database backend
- Minimal file I/O

### Information Hiding

Three levels of encapsulation:
1. **Routes hide HTTP specifics** - Services don't know about HTTP
2. **Services hide algorithms** - Routes don't implement logic
3. **Repository hides data source** - Services don't know about files/DB

## Configuration

### Environment Variables

See `.env.example` for all options. Key ones:

```env
API_HOST=127.0.0.1
API_PORT=5000
API_DEBUG=False
API_RELOAD=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

### Paths

Centralized in `config.py::Settings`:
- All data paths relative to repository root
- Auto-creates directories on startup
- Override via `.env`

## Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "detail": "Descriptive message",
  "message": "Optional context"
}
```

HTTP status codes:
- `200` - Success
- `404` - Not found
- `400` - Validation error
- `500` - Server error

## Testing

Services are designed for easy testing:
- Pure functions with clear inputs/outputs
- Repository injected as dependency
- No global state
- Mockable data sources

Example test structure:
```python
def test_study_recommendation():
    repo = MockRepository()
    service = StudyService(repo)
    targets = service.get_study_recommendation()
    assert len(targets) > 0
```

## Performance Optimizations

1. **Lazy Loading**: Data loaded only when needed
2. **In-Memory Caching**: Reduces file I/O
3. **Batch Operations**: Study getLesson returns multiple items
4. **Pagination**: Large vocabulary sets handled with pages
5. **Streaming**: Audio files streamed (not loaded fully)

## Future Enhancements

- [ ] SQLite/PostgreSQL for persistence
- [ ] User authentication & multi-user support
- [ ] Session history tracking
- [ ] Advanced analytics
- [ ] Batch API operations
- [ ] WebSocket support for real-time updates
- [ ] Rate limiting
- [ ] Metrics/tracing (Prometheus)

## Dependencies

See `requirements.txt`:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-multipart` - Form data support

Install with:
```bash
pip install -r requirements.txt
```

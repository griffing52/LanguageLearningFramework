# Language Learning Framework - Full Stack Guide

Complete setup guide for the interactive Language Learning Framework with web UI and API backend.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   React Web UI (Port 3000)              │
│  • Study Sessions • Vocabulary Browser • Progress      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────┐
│           FastAPI Backend (Port 5000)                   │
│  • Spaced Repetition Algorithm                          │
│  • Vocabulary Management • Audio Serving                │
│  • Progress Tracking                                    │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│        C++ Data Files (Repository)                      │
│  • data/seed/words.txt (vocabulary)                     │
│  • data/seed/lesson1.txt (phrases)                      │
│  • data/state/mem0 (progress)                           │
│  • data/audio/ (pronunciation)                          │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
LanguageLearningFramework/
├── apps/
│   ├── api/                          # FastAPI backend
│   │   ├── app.py                    # Main FastAPI app
│   │   ├── config.py                 # Configuration
│   │   ├── core/
│   │   │   ├── models.py             # Pydantic DTOs
│   │   │   └── constants.py          # Enums & constants
│   │   ├── services/                 # Business logic
│   │   ├── data_access/              # Repository pattern
│   │   ├── api/                      # Route handlers
│   │   ├── utils/                    # Utilities
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   └── web-ui/                       # React Vite frontend
│       ├── src/
│       │   ├── api/                  # API clients
│       │   ├── services/             # Frontend logic
│       │   ├── components/           # React components
│       │   ├── hooks/                # Custom hooks
│       │   ├── styles/               # CSS
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── vite.config.ts
│       ├── Dockerfile
│       ├── nginx.conf
│       └── README.md
│
├── data/                             # C++ backend data
│   ├── seed/                         # Static vocabulary
│   ├── state/                        # Runtime progress
│   └── audio/                        # Generated audio files
│
├── docker-compose.yml                # Containerized setup
├── start-dev.sh                      # Unix startup script
├── start-dev.ps1                     # Windows startup script
└── .env.example                      # Config template
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Development (Local)

#### Option 1: Using Startup Scripts

**Windows:**
```powershell
.\start-dev.ps1
```

**macOS/Linux:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

#### Option 2: Manual Setup

**Terminal 1 - API:**
```bash
cd apps/api
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

**Terminal 2 - UI:**
```bash
cd apps/web-ui
npm install
npm run dev
```

**Access:**
- UI: http://localhost:3000
- API: http://127.0.0.1:5000
- API Docs: http://127.0.0.1:5000/api/docs

### Production (Docker)

```bash
# Build and start all services
docker-compose up --build

# Containers:
# - llf-api: http://localhost:5000
# - llf-ui: http://localhost:3000
# - llf-data-prepare: Initializes data directories

# Stop all services
docker-compose down
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key variables:
- `API_HOST`, `API_PORT` - API server address
- `API_DEBUG`, `API_RELOAD` - Development mode settings
- `VITE_API_URL` - Frontend API endpoint
- `CORS_ORIGINS` - Allowed frontend origins
- `LOG_LEVEL` - Logging verbosity

## Features

### Study Sessions (Interactive Learning)

1. **Adaptive Algorithm**: Spaced repetition based on:
   - Frequency (how many times you've answered correctly)
   - Age (sessions since last study)
   - Complexity (difficulty rating)

2. **Interactive UI** (Similar to Mango Learning/Pimsleur):
   - Word/phrase display with translation
   - Audio pronunciation
   - Confidence feedback (1-5 scale)
   - Immediate progress tracking

3. **Session Flow**:
   - Load lesson plan (10 items by default)
   - Study each item with audio
   - Provide feedback (correct/incorrect + confidence)
   - Automatic progression to next item
   - Progress bar shows completion

### Vocabulary Management

- Browse all words and phrases
- Search functionality
- View frequency and complexity statistics
- Organized word lists

### Progress Dashboard

- Overall learning metrics
- Words/phrases learned percentage
- Achievement milestones
- Real-time progress updates

## API Reference

### Study Endpoints

```
GET  /api/study/next          - Get next study items
POST /api/study/feedback      - Submit study feedback
GET  /api/study/lesson        - Get full lesson plan
```

### Vocabulary Endpoints

```
GET  /api/vocabulary/words                  - List words
GET  /api/vocabulary/words/{value}          - Get specific word
GET  /api/vocabulary/phrases                - List phrases
GET  /api/vocabulary/phrases/{value}        - Get specific phrase
GET  /api/vocabulary/progress               - Get progress snapshot
```

### Audio Endpoints

```
GET  /api/audio/{filename}    - Serve audio file
GET  /api/audio               - List available audio
GET  /api/audio/stats         - Audio library stats
```

### Progress Endpoints

```
GET  /api/progress/snapshot   - Current snapshot
GET  /api/progress/detailed   - Detailed report
```

Full interactive docs: http://127.0.0.1:5000/api/docs

## Data Management

### Loading Data

The API automatically loads:
1. **Words** from `data/seed/words.txt`
   - Format: `word|translation|complexity|frequency|age` (one per line)
2. **Phrases** from `data/seed/lesson1.txt`
   - Format: `phrase|translation|complexity` (one per line)
3. **Progress** from `data/state/mem0`
   - JSON or simple line format

### Saving Progress

Study progress is automatically saved to `data/state/mem0` when:
- You submit study feedback
- The session ends

### Audio Files

Place pronunciation audio in `data/audio/`:
- Format: `{item_type}-{value}.mp3` (e.g., `word-Grüezi.mp3`)
- Supported: MP3, WAV, OGG
- Generated TTS with `tools/tts/tts.py`

## Development

### Adding a Component

1. Create component file in `apps/web-ui/src/components/`
2. Import styles from `src/styles/components.css`
3. Use TypeScript for type safety
4. Export as named export

### Adding an API Endpoint

1. Create service method in `apps/api/services/`
2. Create route handler in `apps/api/api/`
3. Include router in `apps/api/app.py`
4. Test with `/api/docs`

### Backend Architecture

- **Information Hiding**: Services expose only necessary interfaces
- **Separation of Concerns**: Routes → Services → Data Access
- **Repository Pattern**: Clean abstraction over data sources
- **Type Safety**: Pydantic models for all I/O

### Frontend Architecture

- **Single Contact Point**: All API calls through `src/api/client.ts`
- **Service Layer**: Business logic in `src/services/`
- **Custom Hooks**: Encapsulate state and side effects
- **Component Composition**: Small, reusable components

## Testing

TODO: Add pytest (backend) and Jest (frontend) test suites

## Troubleshooting

### UI can't reach API

1. Check API is running: http://127.0.0.1:5000/health
2. Verify CORS origins in `.env` include frontend URL
3. Check `VITE_API_URL` in frontend config

### Audio doesn't play

1. Ensure audio files exist in `data/audio/`
2. Check file naming: `{item_type}-{value}.mp3`
3. Browser may require CORS headers (check server logs)

### Data not loading

1. Verify files exist:
   - `data/seed/words.txt`
   - `data/seed/lesson1.txt`
2. Check file format (pipe-delimited, UTF-8)
3. Review API logs: `LOG_LEVEL=DEBUG` in `.env`

### Performance Issues

- Increase `page_size` to load fewer items initially
- Reduce `lesson_size` for shorter study sessions
- Use production build: `npm run build` (frontend)

## Deployment

### Vercel (Frontend)

```bash
cd apps/web-ui
npm run build
# Deploy dist/ directory to Vercel
```

### Heroku / Railway (Backend)

```bash
# Build base image with Python
docker build -t llf-api ./apps/api
# Push to container registry
# Deploy with PORT environment variable
```

### Self-Hosted Docker

```bash
docker-compose -f docker-compose.yml up -d
# Services available on:
# UI: http://your-domain:3000
# API: http://your-domain:5000
```

## License

[Check LICENSE.txt in repository root]

## Support

- API Documentation: http://127.0.0.1:5000/api/docs
- Frontend README: [apps/web-ui/README.md](apps/web-ui/README.md)
- Backend README: [apps/api/README.md](apps/api/README.md)

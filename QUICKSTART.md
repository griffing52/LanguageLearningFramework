# Quick Start Guide

Get the Language Learning Framework running in 5 minutes.

## Prerequisites

- Python 3.9+
- Node.js 18+

## Start Development Mode

### Windows

```powershell
.\start-dev.ps1
```

### macOS/Linux

```bash
chmod +x start-dev.sh
./start-dev.sh
```

## Access the Application

Once started, open your browser:

- **UI**: http://localhost:3000
- **API**: http://127.0.0.1:5000
- **API Docs**: http://127.0.0.1:5000/api/docs

## What's Running

| Service | Port | Purpose |
|---------|------|---------|
| React UI | 3000 | Interactive study interface |
| FastAPI | 5000 | Backend REST API |

## First Steps

1. **Study**: Click "📚 Study" tab
   - See a word/phrase with translation
   - Click "▶ Pronounce" to hear audio
   - Select confidence level (1-5)
   - Click ✓ or ✗ for feedback

2. **Browse**: Click "📝 Vocabulary" tab
   - See all available words/phrases
   - Search by typing
   - View frequency and complexity

3. **Track Progress**: Click "📊 Progress" tab
   - See learning metrics
   - Track milestones
   - View overall progress

## Customize

Copy `.env.example` to `.env` and adjust:

```bash
cp .env.example .env
```

Key settings:
- `API_PORT` - Change API port (default: 5000)
- `CORS_ORIGINS` - Frontend URLs (for deployment)
- `LOG_LEVEL` - Debug output verbosity

## Generate TTS Audio

To add audio pronunciation:

```bash
cd tools/tts
pip install -r requirements.txt
python tts.py
```

Audio files go to `data/audio/`.

## Troubleshooting

**"Cannot connect to API"**
- Ensure API is running on http://127.0.0.1:5000
- Check `CORS_ORIGINS` in `.env`

**"No audio available"**
- Generate audio files using `tools/tts/tts.py`
- Files go in `data/audio/`

**"Data not loading"**
- Verify `data/seed/words.txt` exists
- Check `data/seed/lesson1.txt` is formatted correctly

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed configuration
- See [API_SPEC.md](API_SPEC.md) for API endpoints
- Check [apps/api/README.md](apps/api/README.md) for backend details
- Check [apps/web-ui/README.md](apps/web-ui/README.md) for frontend details

## Stop Services

Press `Ctrl+C` in each terminal window to stop services.

## Deploy with Docker

```bash
docker-compose up --build
```

Then access:
- UI: http://localhost:3000
- API: http://localhost:5000

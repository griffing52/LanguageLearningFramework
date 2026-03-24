# API Specification

Language Learning Framework REST API specification.

## Base URL

```
http://127.0.0.1:5000/api
```

## Content Type

All requests and responses use `application/json`.

## Response Format

All endpoints follow a consistent response format:

```json
{
  "status": "success|error",
  "data": {...},
  "message": "optional error message"
}
```

## Error Handling

| Status | Description |
|--------|-------------|
| 200 | Success |
| 404 | Not Found |
| 400 | Bad Request (validation error) |
| 500 | Server Error |

Error responses include:
```json
{
  "status": "error",
  "message": "Descriptive error message",
  "detail": "Additional context"
}
```

---

## Endpoints

### Study API

#### Get Next Study Targets

```http
GET /study/next?batch_size=5
```

Returns the next items to study using spaced repetition algorithm.

**Query Parameters:**
- `batch_size` (optional, default: 5, max: 20) - Number of items to return

**Response:**
```json
[
  {
    "target_id": "word-Grüezi",
    "target_type": "word",
    "target_value": "Grüezi",
    "target_translation": "Hello",
    "urgency_score": 0.85,
    "reason": "High frequency, recent age",
    "audio_url": "/api/audio/word-Grüezi.mp3"
  }
]
```

**Usage:**
```typescript
const targets = await studyApi.getNextTargets(5);
```

---

#### Submit Study Feedback

```http
POST /study/feedback
```

Record feedback on a studied item to update learning progress.

**Request Body:**
```json
{
  "target_id": "word-Grüezi",
  "correct": true,
  "confidence": 4,
  "time_spent_seconds": 12
}
```

**Parameters:**
- `target_id` - Format: `word-{value}` or `phrase-{value}`
- `correct` - Boolean: was the answer correct?
- `confidence` - Integer 1-5: user confidence level
- `time_spent_seconds` - Integer: seconds spent on item

**Response:**
```json
{
  "status": "success",
  "message": "Feedback recorded",
  "next_batch": [
    {
      "target_id": "phrase-Guten Morgen",
      "target_type": "phrase",
      ...
    }
  ]
}
```

**Usage:**
```typescript
await studyApi.submitFeedback({
  target_id: "word-Grüezi",
  correct: true,
  confidence: 4,
  time_spent_seconds: 12
});
```

---

#### Get Lesson Plan

```http
GET /study/lesson?lesson_size=10
```

Get a full lesson plan (collection of study targets).

**Query Parameters:**
- `lesson_size` (optional, default: 10, max: 30) - Number of items in lesson

**Response:**
```json
[
  {
    "target_id": "word-Wasser",
    "target_type": "word",
    "target_value": "Wasser",
    "target_translation": "Water",
    "urgency_score": 0.72,
    "reason": "Regular review (frequency: 3)",
    "audio_url": "/api/audio/word-Wasser.mp3"
  },
  ...
]
```

**Usage:**
```typescript
const lesson = await studyApi.getLesson(10);
```

---

### Vocabulary API

#### List Words

```http
GET /vocabulary/words?page=1&page_size=20&search=grüezi
```

Get paginated list of words with optional search.

**Query Parameters:**
- `page` (optional) - Page number (1-indexed)
- `page_size` (optional, default: 20, max: 100) - Items per page
- `search` (optional) - Search query (matches value or translation)

**Response:**
```json
{
  "words": [
    {
      "value": "Grüezi",
      "translation": "Hello",
      "complexity": 1,
      "frequency": 15,
      "age": 30
    }
  ],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "pages": 8
}
```

**Usage:**
```typescript
const result = await vocabularyApi.getWords(1, 20, "grüezi");
```

---

#### Get Specific Word

```http
GET /vocabulary/words/{value}
```

Get details of a specific word.

**Path Parameters:**
- `value` - The word value (URL-encoded)

**Response:**
```json
{
  "value": "Grüezi",
  "translation": "Hello",
  "complexity": 1,
  "frequency": 15,
  "age": 30
}
```

**Usage:**
```typescript
const word = await vocabularyApi.getWord("Grüezi");
```

---

#### Get Word Statistics

```http
GET /vocabulary/words/{value}/stats
```

Get statistics for a word.

**Response:**
```json
{
  "id": "word-Grüezi",
  "value": "Grüezi",
  "item_type": "word",
  "frequency": 15,
  "age": 30,
  "complexity": 1,
  "last_studied": "2026-03-23T14:30:00Z"
}
```

---

#### List Phrases

```http
GET /vocabulary/phrases?page=1&page_size=20&search=guten
```

Get paginated list of phrases with optional search.

**Query Parameters:**
- `page` (optional) - Page number
- `page_size` (optional, default: 20, max: 100)
- `search` (optional) - Search query

**Response:**
```json
{
  "phrases": [
    {
      "value": "Guten Morgen",
      "translation": "Good morning",
      "complexity": 1,
      "frequency": 5,
      "age": 10,
      "words": ["Guten", "Morgen"],
      "dependencies": []
    }
  ],
  "total": 75,
  "page": 1,
  "page_size": 20,
  "pages": 4
}
```

---

#### Get Specific Phrase

```http
GET /vocabulary/phrases/{value}
```

Get details of a specific phrase.

**Response:**
```json
{
  "value": "Guten Morgen",
  "translation": "Good morning",
  "complexity": 1,
  "frequency": 5,
  "age": 10,
  "words": ["Guten", "Morgen"],
  "dependencies": []
}
```

---

#### Get Vocabulary Progress

```http
GET /vocabulary/progress
```

Get overall vocabulary learning progress.

**Response:**
```json
{
  "total_words": 500,
  "words_learned": 145,
  "words_learned_percentage": 29.0,
  "total_phrases": 200,
  "phrases_learned": 32,
  "phrases_learned_percentage": 16.0,
  "average_complexity": 2.3,
  "total_items": 700,
  "items_learned": 177
}
```

---

### Audio API

#### Serve Audio File

```http
GET /audio/{filename}
```

Stream audio file for playback.

**Path Parameters:**
- `filename` - Audio filename (e.g., `word-Grüezi.mp3`)

**Response:**
- Audio file (HTTP 200 with audio/mpeg content-type)
- HTTP 404 if file not found

**Usage:**
```typescript
const audioUrl = audioApi.getAudioUrl("word-Grüezi.mp3");
// Use in <audio> tag or play with audioService
```

---

#### List Audio Files

```http
GET /audio?limit=100
```

List available audio files.

**Query Parameters:**
- `limit` (optional, default: 100) - Maximum files to return

**Response:**
```json
{
  "files": [
    "word-Grüezi.mp3",
    "word-Wasser.mp3",
    "phrase-Guten Morgen.mp3"
  ],
  "count": 3
}
```

---

#### Get Audio Statistics

```http
GET /audio/stats
```

Get statistics about the audio library.

**Response:**
```json
{
  "total_files": 150,
  "formats": {
    ".mp3": 145,
    ".wav": 5
  },
  "audio_dir": "/path/to/data/audio"
}
```

---

### Progress API

#### Get Progress Snapshot

```http
GET /progress/snapshot
```

Get current learning progress snapshot.

**Response:**
```json
{
  "total_words": 500,
  "words_learned": 145,
  "total_phrases": 200,
  "phrases_learned": 32,
  "average_complexity": 2.3,
  "session_count": 48,
  "last_session_time": "2026-03-23T14:30:00Z"
}
```

---

#### Get Detailed Progress Report

```http
GET /progress/detailed
```

Get comprehensive progress report with breakdowns.

**Response:**
```json
{
  "vocabulary": {
    "total_words": 500,
    "words_learned": 145,
    "words_percentage": 29.0,
    "words_remaining": 355
  },
  "phrases": {
    "total_phrases": 200,
    "phrases_learned": 32,
    "phrases_percentage": 16.0,
    "phrases_remaining": 168
  },
  "overall": {
    "total_items": 700,
    "items_learned": 177,
    "items_percentage": 25.3,
    "average_complexity": 2.3
  },
  "milestones": {
    "first_words": true,
    "first_phrases": true,
    "quarter_vocabulary": true,
    "half_vocabulary": false,
    "nearly_done": false
  }
}
```

---

## Spaced Repetition Algorithm

The `/study/next` endpoint uses a scoring algorithm to determine study urgency:

**Scoring Formula:**
```
score = 100 (if frequency == 0)  // Never studied
      + frequency^-1             // Inverse of frequency
      + age * 0.5 (if age > 50)  // Recent urgency boost
      + age * 0.1 (if age <= 50) // Subtle age factor
      + complexity_factor        // Slight preference for simpler items
      + 10 (for phrases)         // Phrase priority
```

**Priority Order:**
1. Never-studied items (frequency = 0)
2. Items needing review (age > threshold)
3. Low-frequency items
4. Phrases over words
5. Simpler items preferred

Items are then randomly shuffled within score tiers to provide variety.

---

## Rate Limiting

No rate limiting currently implemented. For production deployment, consider:
- IP-based rate limiting
- User-account based quotas
- Per-endpoint limits

---

## CORS Configuration

Default CORS allowed origins:
```
http://localhost:3000
http://127.0.0.1:3000
```

Configure via `.env`:
```
CORS_ORIGINS=http://localhost:3000,http://example.com
```

---

## Documentation

Interactive API documentation available at:
- Swagger UI: http://127.0.0.1:5000/api/docs
- ReDoc: http://127.0.0.1:5000/api/redoc
- OpenAPI JSON: http://127.0.0.1:5000/api/openapi.json

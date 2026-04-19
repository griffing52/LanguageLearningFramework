# TTS Server Deployment

This folder now supports running a standalone TTS server on a dedicated machine.

## Supported Methods

- `speecht5`
- `legacy_stitched`
- `orpheus_lora`

The server exposes:

- `GET /health`
- `GET /methods`
- `POST /synthesize`

## Request Format

`POST /synthesize`

```json
{
  "text": "Hoi zame",
  "tts_method": "orpheus_lora",
  "language": "gsw",
  "voice": "default",
  "options": {
    "output_format": "wav"
  }
}
```

## Start On Inference Machine

1. Install dependencies:

```powershell
pip install -r tools/tts/requirements.txt
```

2. Configure environment values from `.env.example`:

- `TTS_SERVER_HOST`
- `TTS_SERVER_PORT`
- `TTS_SERVER_DEFAULT_METHOD`
- `TTS_SPEECHT5_SPEAKER_EMBEDDINGS` (required for SpeechT5)
- `TTS_ORPHEUS_MODEL_ID` and optionally `HF_TOKEN`

3. Start the server:

```powershell
uvicorn tools.tts.server:app --host 0.0.0.0 --port 7001
```

## Connect API Machine To Remote Server

Set these environment values on the API machine:

- `TTS_REMOTE_PROVIDER_ID`
- `TTS_REMOTE_BASE_URL`
- `TTS_REMOTE_SYNTHESIZE_PATH`
- `TTS_REMOTE_HEALTH_PATH`
- `TTS_REMOTE_API_KEY` (optional)
- `TTS_REMOTE_EXTRA_HEADERS` (optional JSON string)

When `tts_providers.json` is empty, the API auto-bootstraps this remote provider from env.

## Selecting Method In UI

In the Platform TTS workspace:

- Choose a method (`speecht5`, `legacy_stitched`, or `orpheus_lora`)
- Select a provider to run remotely
- Or leave provider blank to run local inference in API process

# Remote TTS Inference Server

This guide explains how to run TTS inference on a separate machine and connect it to the main Language Learning Framework API and UI.

## Overview

The project now supports a split deployment:

- API and UI machine: runs the main app stack.
- Inference machine: runs the standalone TTS server.

The main API forwards inference requests to the remote TTS server when a provider is selected.

## What You Need

### API or app machine

- Main Language Learning Framework stack running.
- Network access to the inference machine on the configured TTS server port.

### Inference machine

- Python 3.9+.
- Access to required model assets and tokens.
- Optional GPU if you want faster local model inference.

## Supported Inference Methods

- speecht5
- legacy_stitched
- orpheus_lora

## Step 1: Configure Environment

Use values from the root .env.example file.

### Inference machine variables

- TTS_SERVER_HOST
- TTS_SERVER_PORT
- TTS_SERVER_OUTPUT_DIR
- TTS_SERVER_DEFAULT_METHOD
- TTS_SERVER_RETURN_AUDIO_BASE64

SpeechT5 settings:

- TTS_SPEECHT5_CHECKPOINT
- TTS_SPEECHT5_MODEL
- TTS_SPEECHT5_VOCODER
- TTS_SPEECHT5_SAMPLE_RATE
- TTS_SPEECHT5_SPEAKER_EMBEDDINGS

Legacy settings:

- TTS_LEGACY_ROOT
- TTS_LEGACY_MODE

Orpheus settings:

- TTS_ORPHEUS_MODEL_ID
- TTS_ORPHEUS_ENDPOINT_URL (optional)
- HF_TOKEN

### API machine variables

These bootstrap a remote provider automatically when the provider state file is empty:

- TTS_REMOTE_PROVIDER_ID
- TTS_REMOTE_PROVIDER_NAME
- TTS_REMOTE_BASE_URL
- TTS_REMOTE_SYNTHESIZE_PATH
- TTS_REMOTE_HEALTH_PATH
- TTS_REMOTE_API_KEY (optional)
- TTS_REMOTE_EXTRA_HEADERS (optional JSON object string)

## Step 2: Start the Inference Server

From repository root on the inference machine:

**Option A: Direct uvicorn (Windows/Linux/macOS)**

```bash
pip install -r tools/tts/requirements.txt
uvicorn tools.tts.server:app --host 0.0.0.0 --port 7001
```

**Option B: Python module (alternative)**

```bash
pip install -r tools/tts/requirements.txt
python -m uvicorn tools.tts.server:app --host 0.0.0.0 --port 7001
```

If you use a different port, update `TTS_SERVER_PORT` and `TTS_REMOTE_BASE_URL` accordingly.

## Step 3: Verify the Inference Server

From the API machine:

```powershell
curl http://INFERENCE_HOST:7001/health
curl http://INFERENCE_HOST:7001/methods
```

Expected:

- health returns status ok
- methods returns speecht5, legacy_stitched, and orpheus_lora

## Step 4: Start the Main API and UI

Start the stack normally on the API machine.

For local development:

```powershell
.\start-dev.ps1
```

Or use Docker compose as usual.

## Step 5: Use It in the UI

In Platform TTS Workspace:

1. Pick tts_method.
2. Pick a provider (remote server) if you want remote execution.
3. Run inference.

If provider is left empty for non-provider methods, inference runs in the local API process instead.

## Required Network and Security Setup

- Open inbound access on the inference machine for the TTS server port.
- Restrict access to trusted sources only.
- Prefer private network or VPN between machines.
- If exposing over public network, add an auth layer and TLS at a reverse proxy.

## Troubleshooting

### API cannot reach remote TTS server

- Check TTS_REMOTE_BASE_URL points to reachable host and port.
- Verify firewall rules on the inference machine.
- Confirm server is running and health endpoint responds.

### SpeechT5 fails at runtime

- Ensure TTS_SPEECHT5_SPEAKER_EMBEDDINGS points to a valid file.
- Confirm model and vocoder names are correct and downloadable.

### Orpheus fails at runtime

- Confirm HF_TOKEN has model access when needed.
- Check TTS_ORPHEUS_MODEL_ID or TTS_ORPHEUS_ENDPOINT_URL.

### Legacy method fails

- Confirm submodule exists at tools/tts/SwissGermanLanguage.
- Verify the legacy audio directories and source clips exist.

## Related Docs

- Setup: [setup.md](../setup.md)
- Deployment: [docker.md](docker.md)
- Tooling overview: [tooling.md](../tooling.md)

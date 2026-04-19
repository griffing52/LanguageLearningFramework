"""Bridge between the API layer and the local TTS toolchain."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
import sys


TOOLS_TTS_DIR = Path(__file__).resolve().parents[3] / "tools" / "tts"


def _ensure_tools_tts_path() -> None:
    tools_path = str(TOOLS_TTS_DIR)
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)


def synthesize_local_tts(
    method: str,
    text: str,
    output_path: str | Path,
    *,
    options: Mapping[str, Any] | None = None,
) -> str:
    """Generate local audio by dispatching to the selected backend."""
    _ensure_tools_tts_path()
    options_dict = dict(options or {})
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if method == "speecht5":
        import speecht5_backend

        return speecht5_backend.generate_audio(text, output_path=output_file, **options_dict)

    if method == "legacy_stitched":
        import legacy_backend

        return legacy_backend.generate_audio(text, output_path=output_file, **options_dict)

    if method == "orpheus_lora":
        import orpheus_backend

        return orpheus_backend.generate_audio(text, output_path=output_file, **options_dict)

    raise ValueError(f"Unsupported local TTS method: {method}")

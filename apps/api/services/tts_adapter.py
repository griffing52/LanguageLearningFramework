"""Bridge between the API layer and the local TTS toolchain."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, Mapping
import sys


def _find_repo_root(start_path: Path) -> Path | None:
    current = start_path.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "tools" / "tts").exists():
            return candidate
    return None


_REPO_ROOT = _find_repo_root(Path(__file__).resolve())


def _ensure_tools_tts_path() -> None:
    if not _REPO_ROOT:
        raise ModuleNotFoundError(
            "Local TTS tools are not available in this runtime. "
            "Use a remote provider_id for inference or mount tools/tts into the API environment."
        )

    repo_path = str(_REPO_ROOT)
    if repo_path not in sys.path:
        sys.path.insert(0, repo_path)


def _import_local_backend(module_name: str):
    _ensure_tools_tts_path()
    return import_module(f"tools.tts.{module_name}")


def synthesize_local_tts(
    method: str,
    text: str,
    output_path: str | Path,
    *,
    options: Mapping[str, Any] | None = None,
) -> str:
    """Generate local audio by dispatching to the selected backend."""
    options_dict = dict(options or {})
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if method == "speecht5":
        backend = _import_local_backend("speecht5_backend")

        return backend.generate_audio(text, output_path=output_file, **options_dict)

    if method == "legacy_stitched":
        backend = _import_local_backend("legacy_backend")

        return backend.generate_audio(text, output_path=output_file, **options_dict)

    if method == "orpheus_lora":
        backend = _import_local_backend("orpheus_backend")

        return backend.generate_audio(text, output_path=output_file, **options_dict)

    raise ValueError(f"Unsupported local TTS method: {method}")

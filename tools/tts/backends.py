"""Shared TTS backend selection helpers."""

from __future__ import annotations

from importlib import import_module


REMOTE_PROVIDER_METHOD = "provider"
SPEECHT5_METHOD = "speecht5"
LEGACY_STITCHED_METHOD = "legacy_stitched"
ORPHEUS_LORA_METHOD = "orpheus_lora"

LOCAL_METHODS = {
    SPEECHT5_METHOD,
    LEGACY_STITCHED_METHOD,
    ORPHEUS_LORA_METHOD,
}

METHOD_ALIASES = {
    "remote": REMOTE_PROVIDER_METHOD,
    "remote_provider": REMOTE_PROVIDER_METHOD,
    "provider": REMOTE_PROVIDER_METHOD,
    "speecht5": SPEECHT5_METHOD,
    "legacy": LEGACY_STITCHED_METHOD,
    "legacy_stitched": LEGACY_STITCHED_METHOD,
    "stitched": LEGACY_STITCHED_METHOD,
    "orpheus": ORPHEUS_LORA_METHOD,
    "orpheus_lora": ORPHEUS_LORA_METHOD,
}


def normalize_method(method: str | None) -> str:
    """Normalize a method identifier to the canonical backend name."""
    if not method:
        return REMOTE_PROVIDER_METHOD

    normalized = method.strip().lower()
    return METHOD_ALIASES.get(normalized, normalized)


def is_local_method(method: str | None) -> bool:
    return normalize_method(method) in LOCAL_METHODS


def _import_backend_module(module_name: str):
    """Import backend modules in both package and flat-module execution contexts."""
    if __package__:
        try:
            return import_module(f".{module_name}", package=__package__)
        except ModuleNotFoundError:
            # Fall back to flat imports for direct script usage.
            pass

    return import_module(module_name)


def load_local_backend(method: str):
    normalized = normalize_method(method)
    if normalized == SPEECHT5_METHOD:
        return _import_backend_module("speecht5_backend")
    if normalized == LEGACY_STITCHED_METHOD:
        return _import_backend_module("legacy_backend")
    if normalized == ORPHEUS_LORA_METHOD:
        return _import_backend_module("orpheus_backend")
    raise ValueError(f"Method '{method}' is not a local TTS backend")


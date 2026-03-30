"""
Platform service - cohesive operations spanning vocabulary, lessons, and TTS providers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import json
import urllib.request
import urllib.error

from config import settings
from core.models import (
    CreateLessonRequest,
    CreatePhraseRequest,
    CreateWordRequest,
    LessonDefinition,
    TtsInferenceRequest,
    TtsProviderConfig,
    WordDTO,
    PhraseDTO,
)
from data_access.repository import get_repository, reset_repository
from utils.logger import get_logger

logger = get_logger(__name__)


class PlatformService:
    """Cross-module service for cohesive platform management."""

    def __init__(self):
        self.repo = get_repository()

    def _refresh_repository(self) -> None:
        reset_repository()
        self.repo = get_repository()

    @staticmethod
    def _append_line(file_path: Path, line: str) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as handle:
            handle.write(f"{line}\n")

    def add_word(self, request: CreateWordRequest) -> WordDTO:
        value = request.value.strip()
        if self.repo.get_word(value):
            raise ValueError(f"Word '{value}' already exists")

        # Store in equals format to match seed files: word=translation
        # Complexity, frequency, age are only used when loaded from memory state.
        # New words default to complexity=1, frequency=0, age=0
        line = f"{value}={request.translation.strip()}"
        self._append_line(settings.WORDS_FILE, line)
        self._refresh_repository()

        created = self.repo.get_word(value)
        if not created:
            raise RuntimeError("Word creation did not persist")
        return created

    def add_phrase(self, request: CreatePhraseRequest) -> PhraseDTO:
        value = request.value.strip()
        if self.repo.get_phrase(value):
            raise ValueError(f"Phrase '{value}' already exists")

        # Store in equals format to match seed files: phrase=translation
        # Complexity, frequency, age are only used when loaded from memory state.
        # New phrases default to complexity=1, frequency=0, age=0
        line = f"{value}={request.translation.strip()}"
        self._append_line(settings.LESSONS_FILE, line)
        self._refresh_repository()

        created = self.repo.get_phrase(value)
        if not created:
            raise RuntimeError("Phrase creation did not persist")
        return created

    @staticmethod
    def _decode_upload(content: bytes) -> str:
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError as err:
            raise ValueError("Upload must be UTF-8 text") from err

    @staticmethod
    def _sanitize_text_lines(raw_text: str) -> List[str]:
        return [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    @staticmethod
    def _normalize_vocab_lines(raw_text: str) -> List[str]:
        """
        Normalize vocabulary lines from either equals-separated or pipe-separated format.
        
        Input formats supported:
        - Equals format (data-files.md): word=translation or *word=translation or !word=translation
        - Pipe format (legacy): value|translation|complexity|frequency|age
        
        Output format (always equals): word=translation
        
        Special markers in equals format:
        - * = known word (preserved in output, applies when loaded: complexity=1, frequency=1, age=100)
        - ! = important word (preserved in output, applies when loaded: complexity=2, frequency=0, age=0)
        - no marker = regular word (normal load defaults)
        """
        normalized: List[str] = []
        
        for line in PlatformService._sanitize_text_lines(raw_text):
            # Check if this is equals-separated format
            if '=' in line and '|' not in line:
                # Equals format: [*|!]word=translation - keep as is
                parts = line.split('=', 1)
                if len(parts) != 2:
                    continue
                
                value = parts[0].strip()
                translation = parts[1].strip()
                
                # Remove markers for validation, then re-add if present
                has_marker = False
                marker = ""
                if value.startswith('*') or value.startswith('!'):
                    marker = value[0]
                    clean_value = value[1:].strip()
                    has_marker = True
                else:
                    clean_value = value
                
                if not clean_value or not translation:
                    continue
                
                # Re-add marker if present
                if has_marker:
                    normalized.append(f"{marker}{clean_value}={translation}")
                else:
                    normalized.append(f"{clean_value}={translation}")
            
            # Pipe-separated format (legacy) - convert to equals format
            elif '|' in line:
                parts = [part.strip() for part in line.split("|")]
                if len(parts) < 2:
                    continue

                value = parts[0]
                translation = parts[1]
                # Ignore complexity/frequency/age in pipe format input - not needed for output
                
                normalized.append(f"{value}={translation}")

        if not normalized:
            raise ValueError("No valid entries found. Expected lines in format: word=translation or value|translation")

        return normalized

    @staticmethod
    def _parse_memory_payload(raw_text: str) -> Dict[str, int]:
        cleaned = raw_text.strip()
        if not cleaned:
            return {}

        if cleaned.startswith("{"):
            parsed = json.loads(cleaned)
            return {str(key): int(value) for key, value in parsed.items()}

        memory: Dict[str, int] = {}
        for line in PlatformService._sanitize_text_lines(cleaned):
            parts = [part.strip() for part in line.split("|")]
            if len(parts) < 2:
                continue
            memory[parts[0]] = int(parts[1])
        return memory

    @staticmethod
    def _write_lines(file_path: Path, lines: List[str], mode: str = "replace") -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if mode == "append" and file_path.exists():
            with open(file_path, "a", encoding="utf-8") as handle:
                if file_path.stat().st_size > 0:
                    handle.write("\n")
                handle.write("\n".join(lines))
                handle.write("\n")
            return

        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
            handle.write("\n")

    def import_words(self, content: bytes, mode: str = "replace") -> dict:
        text = self._decode_upload(content)
        lines = self._normalize_vocab_lines(text)
        self._write_lines(settings.WORDS_FILE, lines, mode)
        self._refresh_repository()
        return {
            "kind": "words",
            "mode": mode,
            "imported_entries": len(lines),
            "target_file": str(settings.WORDS_FILE),
            "total_after_import": len(self.repo.get_all_words()),
        }

    def import_phrases(self, content: bytes, mode: str = "replace") -> dict:
        text = self._decode_upload(content)
        lines = self._normalize_vocab_lines(text)
        self._write_lines(settings.LESSONS_FILE, lines, mode)
        self._refresh_repository()
        return {
            "kind": "phrases",
            "mode": mode,
            "imported_entries": len(lines),
            "target_file": str(settings.LESSONS_FILE),
            "total_after_import": len(self.repo.get_all_phrases()),
        }

    def import_memory(self, content: bytes, mode: str = "replace") -> dict:
        text = self._decode_upload(content)
        imported = self._parse_memory_payload(text)
        current_memory = self.repo.get_memory_snapshot()

        merged_memory = current_memory if mode == "append" else {}
        merged_memory.update(imported)

        self._save_json(settings.MEMORY_FILE, merged_memory)
        self._refresh_repository()

        return {
            "kind": "memory",
            "mode": mode,
            "imported_entries": len(imported),
            "target_file": str(settings.MEMORY_FILE),
            "total_after_import": len(self.repo.get_memory_snapshot()),
        }

    def clear_dataset(self, target: str) -> dict:
        if target == "words":
            self._write_lines(settings.WORDS_FILE, [], mode="replace")
        elif target == "phrases":
            self._write_lines(settings.LESSONS_FILE, [], mode="replace")
        elif target == "memory":
            self._save_json(settings.MEMORY_FILE, {})
        elif target == "all":
            self._write_lines(settings.WORDS_FILE, [], mode="replace")
            self._write_lines(settings.LESSONS_FILE, [], mode="replace")
            self._save_json(settings.MEMORY_FILE, {})
        else:
            raise ValueError("target must be one of: words, phrases, memory, all")

        self._refresh_repository()
        return {
            "status": "success",
            "cleared": target,
            "counts": {
                "words": len(self.repo.get_all_words()),
                "phrases": len(self.repo.get_all_phrases()),
                "memory_entries": len(self.repo.get_memory_snapshot()),
            },
        }

    def save_memory_state(self, export_file_name: Optional[str] = None) -> dict:
        snapshot = self.repo.get_memory_snapshot()
        self._save_json(settings.MEMORY_FILE, snapshot)

        export_path: Optional[Path] = None
        if export_file_name:
            safe_name = Path(export_file_name).name
            export_path = settings.STATE_DIR / safe_name
            self._save_json(export_path, snapshot)

        return {
            "status": "success",
            "entries": len(snapshot),
            "saved_file": str(settings.MEMORY_FILE),
            "export_file": str(export_path) if export_path else None,
        }

    def get_teaching_statistics(self, top_n: int = 10) -> dict:
        top_n = max(1, min(top_n, 50))
        return self.repo.get_teaching_statistics(top_n=top_n)

    @staticmethod
    def _load_json(path: Path, default_value: dict) -> dict:
        if not path.exists():
            return default_value
        with open(path, "r", encoding="utf-8") as handle:
            raw = handle.read().strip()
            if not raw:
                return default_value
            return json.loads(raw)

    @staticmethod
    def _save_json(path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

    def list_lessons(self) -> List[LessonDefinition]:
        payload = self._load_json(settings.LESSONS_CATALOG_FILE, {"lessons": []})
        return [LessonDefinition(**item) for item in payload.get("lessons", [])]

    def create_lesson(self, request: CreateLessonRequest) -> LessonDefinition:
        payload = self._load_json(settings.LESSONS_CATALOG_FILE, {"lessons": []})
        lessons = payload.get("lessons", [])

        if any(item.get("lesson_id") == request.lesson_id for item in lessons):
            raise ValueError(f"Lesson '{request.lesson_id}' already exists")

        for entry in request.items:
            if entry.item_type not in {"word", "phrase"}:
                raise ValueError(f"Invalid item_type '{entry.item_type}'")
            if entry.item_type == "word" and not self.repo.get_word(entry.value):
                raise ValueError(f"Word '{entry.value}' not found")
            if entry.item_type == "phrase" and not self.repo.get_phrase(entry.value):
                raise ValueError(f"Phrase '{entry.value}' not found")

        lesson = LessonDefinition(
            lesson_id=request.lesson_id,
            name=request.name,
            description=request.description,
            items=request.items,
        )
        lessons.append(lesson.model_dump())
        payload["lessons"] = lessons
        self._save_json(settings.LESSONS_CATALOG_FILE, payload)
        return lesson

    def list_tts_providers(self) -> dict:
        return self._load_json(settings.TTS_PROVIDERS_FILE, {"default_provider": None, "providers": []})

    def upsert_tts_provider(self, provider: TtsProviderConfig) -> dict:
        payload = self.list_tts_providers()
        providers = payload.get("providers", [])

        updated = False
        for idx, item in enumerate(providers):
            if item.get("provider_id") == provider.provider_id:
                providers[idx] = provider.model_dump()
                updated = True
                break

        if not updated:
            providers.append(provider.model_dump())

        if not payload.get("default_provider"):
            payload["default_provider"] = provider.provider_id

        payload["providers"] = providers
        self._save_json(settings.TTS_PROVIDERS_FILE, payload)
        return payload

    def set_default_provider(self, provider_id: str) -> dict:
        payload = self.list_tts_providers()
        providers = payload.get("providers", [])
        if not any(item.get("provider_id") == provider_id for item in providers):
            raise ValueError(f"Provider '{provider_id}' not found")
        payload["default_provider"] = provider_id
        self._save_json(settings.TTS_PROVIDERS_FILE, payload)
        return payload

    def run_tts_inference(self, request: TtsInferenceRequest) -> dict:
        payload = self.list_tts_providers()
        providers = payload.get("providers", [])
        provider: Optional[dict] = next(
            (item for item in providers if item.get("provider_id") == request.provider_id and item.get("enabled", True)),
            None,
        )

        if not provider:
            raise ValueError(f"Provider '{request.provider_id}' not found or disabled")

        base_url = provider.get("base_url", "").rstrip("/")
        synthesize_path = provider.get("synthesize_path", "/synthesize")
        url = f"{base_url}{synthesize_path}"

        headers = {"Content-Type": "application/json"}
        headers.update(provider.get("extra_headers", {}))
        if provider.get("api_key"):
            headers["Authorization"] = f"Bearer {provider['api_key']}"

        body = {
            "text": request.text,
            "language": request.language,
            "voice": request.voice,
            "options": request.options,
        }

        req = urllib.request.Request(
            url=url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                raw = response.read().decode("utf-8")
                content_type = response.headers.get("Content-Type", "")
                parsed = json.loads(raw) if "application/json" in content_type else {"raw": raw}
                return {
                    "status": "success",
                    "provider_id": provider.get("provider_id"),
                    "url": url,
                    "response": parsed,
                }
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", errors="ignore")
            logger.error("TTS HTTP error from %s: %s", url, detail)
            raise RuntimeError(f"Provider HTTP error {err.code}: {detail}") from err
        except urllib.error.URLError as err:
            logger.error("TTS provider connection error to %s: %s", url, err)
            raise RuntimeError(f"Provider connection error: {err.reason}") from err

    def get_platform_status(self) -> dict:
        words = self.repo.get_all_words()
        phrases = self.repo.get_all_phrases()
        lessons = self.list_lessons()
        tts_payload = self.list_tts_providers()
        memory_entries = self.repo.get_memory_snapshot()

        return {
            "counts": {
                "words": len(words),
                "phrases": len(phrases),
                "lessons": len(lessons),
                "tts_providers": len(tts_payload.get("providers", [])),
                "memory_entries": len(memory_entries),
            },
            "paths": {
                "words_file": str(settings.WORDS_FILE),
                "phrases_file": str(settings.LESSONS_FILE),
                "lessons_catalog_file": str(settings.LESSONS_CATALOG_FILE),
                "tts_providers_file": str(settings.TTS_PROVIDERS_FILE),
                "audio_dir": str(settings.AUDIO_DIR),
            },
            "tts_default_provider": tts_payload.get("default_provider"),
        }

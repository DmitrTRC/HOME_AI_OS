"""
Ollama Provider — локальный AI для чувствительных данных.

Ollama — это runtime для запуска LLM-моделей локально.
Данные НИКОГДА не покидают твой сервер.

Используется для:
- Медицинских записей (sensitivity >= 2)
- Regulated items (sensitivity >= 2)
- Любых данных которые не должны уходить в облако

Модели: Qwen2.5 7B, Mistral 7B, LLaMA 3.1 8B — все бесплатные.
"""

import json

import structlog

from src.core.ai.schemas import (
    ClassifyRequest,
    ClassifyResult,
    ExtractedEntity,
    ExtractRequest,
    ExtractResult,
    SummarizeRequest,
    SummarizeResult,
)
from src.core.config import settings

logger = structlog.get_logger()


class OllamaProvider:
    """
    Локальный AI-провайдер через Ollama.

    Phase 0: базовая реализация.
    Будет расширен в Phase 1-2 для полноценной работы.
    """

    def __init__(self):
        self._host = settings.OLLAMA_HOST
        self._model = settings.OLLAMA_MODEL

    async def _ask(self, prompt: str) -> str:
        """Вызов Ollama API."""
        try:
            import ollama as ollama_lib

            # Ollama Python client
            client = ollama_lib.AsyncClient(host=self._host)
            response = await client.chat(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response["message"]["content"]
        except ImportError:
            logger.error("ollama_not_installed", hint="pip install ollama")
            raise
        except Exception as e:
            logger.error("ollama_api_error", error=str(e), host=self._host)
            raise

    async def classify(self, request: ClassifyRequest) -> ClassifyResult:
        """Классификация через локальную модель."""
        prompt = (
            f"Классифицируй текст по домену. Домены: {', '.join(request.options)}.\n"
            f"Текст: {request.text[:500]}\n\n"
            f'Ответь JSON: {{"domain": "...", "entity_type": "note", "confidence": 0.5}}'
        )
        raw = await self._ask(prompt)

        try:
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(clean)
            return ClassifyResult(**data)
        except Exception:
            return ClassifyResult(domain="knowledge", entity_type="note", confidence=0.1)

    async def extract_entities(self, request: ExtractRequest) -> ExtractResult:
        """Извлечение сущностей через локальную модель."""
        prompt = (
            f"Извлеки сущности из текста: {', '.join(request.extract_types)}.\n"
            f"Текст: {request.text[:500]}\n\n"
            f'JSON: {{"entities": [{{"entity_type": "...", "value": "...", "confidence": 0.5}}]}}'
        )
        raw = await self._ask(prompt)

        try:
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(clean)
            return ExtractResult(
                entities=[ExtractedEntity(**e) for e in data.get("entities", [])]
            )
        except Exception:
            return ExtractResult(entities=[])

    async def summarize(self, request: SummarizeRequest) -> SummarizeResult:
        """Суммаризация через локальную модель."""
        prompt = f"Кратко резюмируй текст:\n{request.text[:1000]}\n\nОтветь 2-3 предложения."
        raw = await self._ask(prompt)
        return SummarizeResult(summary=raw.strip(), key_points=[])

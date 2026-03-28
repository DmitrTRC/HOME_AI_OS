"""
AI Router — выбирает провайдера по задаче и чувствительности данных.

Это реализация паттерна Strategy + Factory.
Аналогия из старого мира: как vtable в C++ — вызываешь метод через интерфейс,
а конкретная реализация подставляется в runtime.

Правила маршрутизации (из ТЗ):
- sensitivity >= SENSITIVE → только локальный AI (Ollama)
- transcribe → всегда Whisper (локальный)
- embed → всегда локальные embeddings
- остальное → Claude API (лучше качество)
"""

from typing import Protocol, runtime_checkable

import structlog

from src.core.ai.schemas import (
    AITaskType,
    ClassifyRequest,
    ClassifyResult,
    ExtractRequest,
    ExtractResult,
    SensitivityLevel,
    SummarizeRequest,
    SummarizeResult,
)

logger = structlog.get_logger()


@runtime_checkable
class AIProvider(Protocol):
    """
    Интерфейс AI-провайдера.

    Protocol в Python — как interface в Java/C#.
    Любой класс который реализует эти методы — подходит.
    Не нужно явное наследование.

    Это ключ к FR-AI-002 и FR-AI-003 из ТЗ:
    "Система НЕ ДОЛЖНА быть жестко привязана к одной модели"
    "Система ДОЛЖНА поддерживать заменяемость model/provider-слотов"
    """

    async def classify(self, request: ClassifyRequest) -> ClassifyResult:
        """Классифицировать текст по домену/типу."""
        ...

    async def extract_entities(self, request: ExtractRequest) -> ExtractResult:
        """Извлечь сущности из текста."""
        ...

    async def summarize(self, request: SummarizeRequest) -> SummarizeResult:
        """Суммаризировать текст."""
        ...


class AIRouter:
    """
    Маршрутизатор AI-задач.

    Решает какой провайдер будет обрабатывать запрос:
    - Claude API — для обычных данных (лучше качество)
    - Ollama — для чувствительных данных (данные не покидают сервер)
    - Whisper — для транскрибации (всегда локально)
    """

    def __init__(
        self,
        cloud_provider: AIProvider | None = None,
        local_provider: AIProvider | None = None,
    ):
        self._cloud = cloud_provider
        self._local = local_provider

    def get_provider(
        self,
        task_type: AITaskType,
        sensitivity: SensitivityLevel = SensitivityLevel.NORMAL,
    ) -> AIProvider:
        """
        Выбрать провайдера по задаче и чувствительности.

        Логика:
        1. Чувствительные данные → ТОЛЬКО локальный
        2. Транскрибация → ТОЛЬКО локальный (Whisper)
        3. Всё остальное → облако (Claude), если доступен
        4. Если облако недоступен → fallback на локальный
        """
        # Чувствительные данные — никогда не отправляем в облако
        if sensitivity >= SensitivityLevel.SENSITIVE:
            if self._local is None:
                raise RuntimeError(
                    f"Local AI provider required for sensitivity={sensitivity}, "
                    "but not configured. Set OLLAMA_HOST in .env"
                )
            logger.info(
                "ai_route_local",
                task=task_type,
                reason="sensitivity",
                sensitivity=sensitivity,
            )
            return self._local

        # Транскрибация — всегда локально (Whisper)
        if task_type == AITaskType.TRANSCRIBE:
            if self._local:
                return self._local
            raise RuntimeError("Whisper not configured for transcription")

        # Обычные данные — облако (лучше качество), fallback на локальный
        if self._cloud is not None:
            return self._cloud

        if self._local is not None:
            logger.warning("ai_fallback_local", task=task_type, reason="cloud_unavailable")
            return self._local

        raise RuntimeError(
            "No AI provider configured. Set ANTHROPIC_API_KEY or OLLAMA_HOST in .env"
        )

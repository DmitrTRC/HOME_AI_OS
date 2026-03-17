"""
Claude AI Provider — реализация через Anthropic API.

Используется для обычных (не чувствительных) данных.
Даёт лучшее качество классификации, извлечения и суммаризации.

Вся работа с Claude API сводится к:
1. Собрать prompt (системный + пользовательский)
2. Отправить HTTP-запрос
3. Распарсить ответ в наши Pydantic-схемы
"""

import json

import anthropic
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


class ClaudeProvider:
    """
    AI-провайдер на базе Claude (Anthropic API).

    Реализует интерфейс AIProvider (через duck typing — Protocol).
    Не нужно писать `class ClaudeProvider(AIProvider)` —
    Python проверит соответствие по наличию методов.
    """

    def __init__(self):
        self._client = anthropic.AsyncAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
        )
        self._model = settings.ANTHROPIC_MODEL

    async def _ask(self, system: str, user: str) -> str:
        """Базовый вызов Claude API. Возвращает текст ответа."""
        try:
            response = await self._client.messages.create(
                model=self._model,
                max_tokens=2000,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error("claude_api_error", error=str(e))
            raise

    async def classify(self, request: ClassifyRequest) -> ClassifyResult:
        """Классифицировать текст по домену."""
        system = (
            "Ты — классификатор входящих данных для персональной операционной системы. "
            "Определи к какому домену относится текст и какой тип сущности создать. "
            "Отвечай ТОЛЬКО валидным JSON без markdown."
        )
        user = (
            f"Текст для классификации:\n{request.text}\n\n"
            f"Доступные домены: {', '.join(request.options)}\n\n"
            f"Доступные типы сущностей: note, task, idea, research, event, "
            f"asset, document, person, reminder\n\n"
            f'Ответ в JSON: {{"domain": "...", "entity_type": "...", '
            f'"confidence": 0.0-1.0, "reasoning": "..."}}'
        )

        raw = await self._ask(system, user)

        try:
            # Убираем возможные markdown-обёртки
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(clean)
            return ClassifyResult(**data)
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("classify_parse_error", raw_response=raw[:200], error=str(e))
            return ClassifyResult(
                domain="knowledge",
                entity_type="note",
                confidence=0.1,
                reasoning=f"Fallback: не удалось распарсить ответ AI: {str(e)[:100]}",
            )

    async def extract_entities(self, request: ExtractRequest) -> ExtractResult:
        """Извлечь сущности из текста."""
        system = (
            "Ты — экстрактор сущностей. Извлекай из текста: людей, даты, организации, "
            "места, темы и другие значимые сущности. "
            "Отвечай ТОЛЬКО валидным JSON без markdown."
        )
        user = (
            f"Текст:\n{request.text}\n\n"
            f"Извлечь типы: {', '.join(request.extract_types)}\n\n"
            f'Ответ в JSON: {{"entities": [{{"entity_type": "...", "value": "...", '
            f'"confidence": 0.0-1.0, "context": "фрагмент текста"}}]}}'
        )

        raw = await self._ask(system, user)

        try:
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(clean)
            entities = [ExtractedEntity(**e) for e in data.get("entities", [])]
            return ExtractResult(entities=entities)
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("extract_parse_error", raw_response=raw[:200], error=str(e))
            return ExtractResult(entities=[])

    async def summarize(self, request: SummarizeRequest) -> SummarizeResult:
        """Суммаризировать текст."""
        style_instructions = {
            "brief": "Дай краткое резюме в 2-3 предложения.",
            "detailed": "Дай подробное резюме с основными деталями.",
            "bullet_points": "Дай резюме в виде ключевых пунктов.",
        }

        system = (
            "Ты — суммаризатор текста для персональной базы знаний. "
            "Отвечай ТОЛЬКО валидным JSON без markdown."
        )
        user = (
            f"Текст:\n{request.text}\n\n"
            f"Стиль: {style_instructions.get(request.style, style_instructions['brief'])}\n\n"
            f'Ответ в JSON: {{"summary": "...", "key_points": ["...", "..."]}}'
        )

        raw = await self._ask(system, user)

        try:
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(clean)
            return SummarizeResult(**data)
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("summarize_parse_error", raw_response=raw[:200], error=str(e))
            return SummarizeResult(summary=request.text[:200] + "...", key_points=[])

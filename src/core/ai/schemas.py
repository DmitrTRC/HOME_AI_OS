"""
Схемы ввода/вывода для AI-операций.

Pydantic-модели которые описывают ЧТО мы просим от AI
и ЧТО получаем в ответ. Независимо от провайдера (Claude, Ollama, Whisper).
"""

from enum import Enum, StrEnum

from pydantic import BaseModel, Field


class SensitivityLevel(int, Enum):
    """Уровень чувствительности данных."""
    NORMAL = 0       # Обычные данные — можно в облако
    INTERNAL = 1     # Внутренние — можно в облако
    SENSITIVE = 2    # Чувствительные — только локальный AI
    RESTRICTED = 3   # Ограниченные — только локальный AI


class AITaskType(StrEnum):
    """Типы AI-задач (из ТЗ: FR-AI-006)."""
    CLASSIFY = "classify"           # Определить домен/тип
    EXTRACT = "extract"             # Извлечь сущности из текста
    SUMMARIZE = "summarize"         # Краткое содержание
    TRANSCRIBE = "transcribe"       # Аудио → текст
    EMBED = "embed"                 # Текст → вектор (для поиска)
    DRAFT = "draft"                 # Черновик текста/отчёта
    DESCRIBE_IMAGE = "describe_image"  # Описание фото


class ClassifyRequest(BaseModel):
    """Запрос на классификацию текста."""
    text: str
    options: list[str] = Field(
        description="Список доменов для классификации",
        default=[
            "knowledge", "medical", "vehicles", "operations",
            "creative", "dev", "registry", "tasks",
        ]
    )


class ClassifyResult(BaseModel):
    """Результат классификации."""
    domain: str                     # Определённый домен
    entity_type: str | None = None  # Предполагаемый тип сущности
    confidence: float = 0.0         # Уверенность (0.0 — 1.0)
    reasoning: str | None = None    # Почему так решили


class ExtractRequest(BaseModel):
    """Запрос на извлечение сущностей."""
    text: str
    extract_types: list[str] = Field(
        default=["person", "date", "organization", "location", "topic"],
        description="Какие типы сущностей извлекать",
    )


class ExtractedEntity(BaseModel):
    """Одна извлечённая сущность."""
    entity_type: str
    value: str
    confidence: float = 0.0
    context: str | None = None      # Фрагмент текста откуда извлечено


class ExtractResult(BaseModel):
    """Результат извлечения."""
    entities: list[ExtractedEntity]


class SummarizeRequest(BaseModel):
    """Запрос на суммаризацию."""
    text: str
    style: str = "brief"            # brief, detailed, bullet_points
    max_length: int | None = None   # Макс. длина в символах


class SummarizeResult(BaseModel):
    """Результат суммаризации."""
    summary: str
    key_points: list[str] = []


class TranscribeResult(BaseModel):
    """Результат транскрибации аудио."""
    text: str
    language: str | None = None
    duration_seconds: float | None = None
    segments: list[dict] = []       # Сегменты с таймкодами

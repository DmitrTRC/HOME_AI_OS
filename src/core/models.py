"""
Базовые модели данных и миксины.

Миксин — это набор полей, который можно "подмешать" в любую модель.
Вместо того чтобы в каждой таблице писать created_at, updated_at —
наследуемся от TimestampMixin и получаем их автоматически.

SQLAlchemy 2.0 style:
- Mapped[тип] — типизированное поле
- mapped_column() — настройка колонки
- relationship() — связь между таблицами
"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, SmallInteger, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class TimestampMixin:
    """Миксин: автоматические created_at и updated_at."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # БД сама ставит время при INSERT
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),         # БД обновляет при UPDATE
        nullable=False,
    )


class AuditMixin:
    """
    Миксин: поля для аудита (кто создал, откуда пришло).
    Используется для чувствительных данных (medical, regulated items).
    """

    source_channel: Mapped[str | None] = mapped_column(
        String(50), nullable=True, doc="Канал поступления: telegram, mail, upload, api"
    )
    source_ref: Mapped[str | None] = mapped_column(
        String(500), nullable=True, doc="Ссылка на источник (message_id, email_id, и т.д.)"
    )


class Entity(Base, TimestampMixin, AuditMixin):
    """
    Главная таблица системы — универсальная сущность.

    Все объекты системы (заметки, задачи, активы, документы, медиа...)
    являются записями в этой таблице. Доменные данные — в поле meta (JSONB).

    Почему одна таблица, а не 20 разных:
    1. Глобальный поиск работает по одной таблице — просто и быстро
    2. Связи между любыми объектами — через entity_links
    3. Теги, аудит, AI-артефакты — единообразно
    4. Доменные поля в JSONB — гибкость без миграций

    Для доменов с жёсткой структурой (medical, vehicles) будут
    дополнительные таблицы со ссылкой entity_id → entities.id
    """

    __tablename__ = "entities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Тип сущности: note, task, asset, document, media, person, pet, ...
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
    )

    # Домен: knowledge, medical, vehicles, operations, dev, ...
    domain: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
    )

    # Основные поля
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Чувствительность: 0=normal, 1=internal, 2=sensitive, 3=restricted
    sensitivity: Mapped[int] = mapped_column(
        SmallInteger, default=0, nullable=False,
    )

    # Статус: active, archived, deleted, draft, finalized
    status: Mapped[str] = mapped_column(
        String(30), default="active", nullable=False,
    )

    # Владелец (пока простая строка, потом — FK на users)
    owner: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # JSONB — гибкие поля для каждого домена
    # Пример для vehicle: {"vin": "...", "plate": "...", "make": "Toyota"}
    # Пример для note: {"mood": "research", "confidence": 0.8}
    meta: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default="{}", nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Entity {self.entity_type}/{self.domain}: {self.title or self.id}>"


class EntityLink(Base, TimestampMixin):
    """
    Связь между двумя сущностями.

    Типы связей: related, source_of, derived_from, contradicts,
    continues, parent, child, attachment, evidence, ...
    """

    __tablename__ = "entity_links"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
    )
    link_type: Mapped[str] = mapped_column(String(50), nullable=False)
    meta: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default="{}", nullable=False,
    )


class Tag(Base):
    """Тег для категоризации сущностей."""

    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    domain: Mapped[str | None] = mapped_column(String(50), nullable=True)


class EntityTag(Base):
    """Связь сущность ↔ тег (many-to-many)."""

    __tablename__ = "entity_tags"

    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True,
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True,
    )


class AIArtifact(Base, TimestampMixin):
    """
    Результат AI-обработки — ОТДЕЛЬНО от исходных данных.

    Это ключевое требование из ТЗ (AC-011):
    AI-артефакты никогда не подменяют исходные данные.
    Всегда можно увидеть что было на входе и что выдал AI.
    Всегда можно перегенерировать.
    """

    __tablename__ = "ai_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True,
    )

    # Тип: summary, classification, extraction, transcription, draft, embedding
    artifact_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Какая модель сгенерировала: claude-sonnet, ollama-qwen, whisper, ...
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Хеш входных данных — для повторной генерации
    input_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Результат AI (JSONB — может быть разная структура)
    content: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Уверенность модели (0.0 — 1.0)
    confidence: Mapped[float | None] = mapped_column(nullable=True)


class AuditLog(Base):
    """
    Журнал аудита — append-only (только добавление, без удаления).

    Записывает кто, что, когда и откуда сделал.
    Критично для чувствительных доменов (medical, regulated items).
    """

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True,
    )
    actor_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    actor_type: Mapped[str] = mapped_column(
        String(20), nullable=False, doc="user, ai, system"
    )
    action: Mapped[str] = mapped_column(
        String(50), nullable=False, doc="create, update, delete, export, ai_process"
    )
    details: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )


class InboxItem(Base, TimestampMixin):
    """
    Элемент входящего буфера (capture inbox).

    Когда пользователь отправляет что-то в Telegram/почту/upload —
    сначала создаётся InboxItem. Потом AI обрабатывает его и создаёт
    сущность в нужном домене.

    Жизненный цикл:
    1. pending — только что поступил
    2. processing — AI обрабатывает
    3. processed — создана сущность (entity_id заполнен)
    4. failed — ошибка обработки
    5. skipped — пользователь отклонил
    """

    __tablename__ = "inbox_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )

    # Откуда пришло
    channel: Mapped[str] = mapped_column(
        String(30), nullable=False, doc="telegram, mail, upload, api"
    )

    # Тип содержимого
    content_type: Mapped[str] = mapped_column(
        String(30), nullable=False, doc="text, voice, photo, video, document"
    )

    # Текстовое содержимое (для text) или транскрипция (для voice)
    raw_content: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Ключ файла в S3 (для media/documents)
    raw_file_key: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # AI-подсказка: в какой домен направить
    suggested_domain: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Статус обработки
    processing_status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False,
    )

    # После обработки — ссылка на созданную сущность
    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

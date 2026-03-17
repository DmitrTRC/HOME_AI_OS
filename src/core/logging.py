"""
Настройка структурированного логирования.

structlog vs обычный logging:
- Обычный: "User 123 created note abc"  (строка, трудно парсить)
- structlog: {"event": "note_created", "user_id": 123, "note_id": "abc"}  (JSON, легко искать)

В dev-режиме логи красиво раскрашены в консоли.
В prod-режиме — JSON для систем мониторинга (Loki, ELK).

Использование:
    import structlog
    logger = structlog.get_logger()

    logger.info("note_created", note_id=note.id, domain="knowledge")
    logger.error("ai_processing_failed", error=str(e), inbox_id=item.id)
"""

import logging
import structlog

from src.core.config import settings


def setup_logging() -> None:
    """Настроить логирование для всего приложения. Вызывается один раз при старте."""

    # Общий уровень логирования
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Выбираем формат вывода
    if settings.LOG_FORMAT == "json":
        # Prod: JSON — для Loki/ELK/Grafana
        renderer = structlog.processors.JSONRenderer()
    else:
        # Dev: красивый цветной вывод в консоль
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            # Добавляет уровень лога (info, error, ...)
            structlog.stdlib.add_log_level,
            # Добавляет timestamp
            structlog.processors.TimeStamper(fmt="iso"),
            # Добавляет имя модуля
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                ]
            ),
            # Форматируем стек-трейсы
            structlog.processors.format_exc_info,
            # Финальный рендеринг
            renderer,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Настраиваем стандартный logging (для сторонних библиотек)
    logging.basicConfig(level=log_level, format="%(message)s")

    # Приглушаем шумные библиотеки
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.APP_DEBUG else logging.WARNING
    )

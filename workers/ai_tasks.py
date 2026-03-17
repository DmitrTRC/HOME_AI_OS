"""
AI-задачи для фоновой обработки.

Эти функции вызываются через Celery когда нужно:
- Классифицировать входящее сообщение
- Извлечь сущности из текста
- Суммаризировать документ
- Транскрибировать аудио

Каждая функция декорирована @celery_app.task — это превращает
обычную функцию в «задачу», которую можно поставить в очередь.

Вызов из другого кода:
    from workers.ai_tasks import process_inbox_item
    process_inbox_item.delay(inbox_item_id)  # .delay() = "поставь в очередь"
"""

import asyncio

import structlog

from workers.celery_app import celery_app

logger = structlog.get_logger()


@celery_app.task(
    bind=True,           # self = ссылка на задачу (для retry)
    max_retries=3,       # Максимум 3 попытки
    default_retry_delay=30,  # Пауза между попытками — 30 сек
)
def process_inbox_item(self, inbox_item_id: str) -> dict:
    """
    Обработать элемент из inbox.

    Жизненный цикл:
    1. Загрузить InboxItem из БД
    2. Если есть файл — скачать из S3
    3. Если аудио — транскрибировать (Whisper)
    4. Классифицировать текст → определить домен
    5. Извлечь сущности
    6. Создать Entity в нужном домене
    7. Обновить InboxItem.status = "processed"

    Пока — заглушка. Реализация в Phase 1.
    """
    logger.info("process_inbox_start", inbox_item_id=inbox_item_id)

    try:
        # TODO Phase 1: полная реализация
        # async def _process():
        #     async with async_session() as db:
        #         item = await db.get(InboxItem, inbox_item_id)
        #         ...
        # asyncio.run(_process())

        logger.info("process_inbox_done", inbox_item_id=inbox_item_id)
        return {"status": "processed", "inbox_item_id": inbox_item_id}

    except Exception as exc:
        logger.error(
            "process_inbox_error",
            inbox_item_id=inbox_item_id,
            error=str(exc),
            retry=self.request.retries,
        )
        # Ставим задачу на повторную попытку
        raise self.retry(exc=exc)


@celery_app.task
def generate_summary(entity_id: str, text: str) -> dict:
    """Сгенерировать AI-summary для сущности. Phase 1."""
    logger.info("generate_summary", entity_id=entity_id)
    # TODO Phase 1
    return {"status": "stub", "entity_id": entity_id}


@celery_app.task
def transcribe_audio(inbox_item_id: str, s3_key: str) -> dict:
    """Транскрибировать аудиофайл через Whisper. Phase 1."""
    logger.info("transcribe_audio", inbox_item_id=inbox_item_id, s3_key=s3_key)
    # TODO Phase 1
    return {"status": "stub", "inbox_item_id": inbox_item_id}

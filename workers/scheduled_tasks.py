"""
Периодические задачи (запускаются по расписанию через Celery Beat).
"""

import structlog

from workers.celery_app import celery_app

logger = structlog.get_logger()


@celery_app.task
def check_reminders() -> dict:
    """
    Проверить просроченные и предстоящие напоминания.
    Отправить уведомления в Telegram.

    Запускается каждый час через Celery Beat.
    Реализация в Phase 3.
    """
    logger.info("check_reminders_start")
    # TODO Phase 3: query reminders table, send notifications
    return {"status": "stub", "checked": 0}


@celery_app.task
def generate_weekly_digest() -> dict:
    """
    Сформировать еженедельный дайджест.

    Содержит: новые заметки, открытые задачи, просроченные сроки,
    медицинские события, активные проекты.

    Запускается по понедельникам в 9:00.
    Реализация в Phase 4.
    """
    logger.info("weekly_digest_start")
    # TODO Phase 4
    return {"status": "stub"}

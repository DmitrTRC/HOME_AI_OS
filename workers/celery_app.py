"""
Celery — распределённая очередь задач.

Аналогия из старого мира: это как cron + message queue в одном.
Но вместо "запусти скрипт в 3 ночи" — "положи задачу в очередь,
worker заберёт и выполнит когда сможет".

Зачем:
- AI-обработка занимает 5-30 секунд — нельзя блокировать HTTP-запрос
- Пользователь отправил фото в Telegram → бот мгновенно ответил "принял"
  → worker в фоне: скачал фото, прогнал OCR, классифицировал, создал запись

Как работает:
1. Код кладёт задачу в Redis (broker): task_name + аргументы
2. Celery worker забирает задачу из Redis
3. Выполняет функцию
4. Результат (если нужен) кладёт обратно в Redis (result backend)

Celery Beat — планировщик:
- Каждый час проверяй напоминания
- Каждый понедельник собирай weekly digest
- Каждые 5 минут проверяй почту
"""

from celery import Celery
from celery.schedules import crontab

from src.core.config import settings

# Создаём экземпляр Celery
celery_app = Celery(
    "home_ai_os",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Настройки
celery_app.conf.update(
    # Сериализация задач в JSON (безопасно и читаемо)
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # Таймзона
    timezone="Europe/Moscow",
    enable_utc=True,

    # Таймауты
    task_soft_time_limit=300,   # 5 минут — мягкий лимит (предупреждение)
    task_time_limit=600,        # 10 минут — жёсткий лимит (убить задачу)

    # Retry при сбоях
    task_acks_late=True,        # Подтверждать задачу ПОСЛЕ выполнения
    worker_prefetch_multiplier=1,  # Брать по одной задаче (для тяжёлых AI-задач)
)

# Автоматически находим задачи в модулях workers/
celery_app.autodiscover_tasks(["workers"])

# --- Периодические задачи (Celery Beat) ---
celery_app.conf.beat_schedule = {
    # Проверка напоминаний каждый час
    "check-reminders": {
        "task": "workers.scheduled_tasks.check_reminders",
        "schedule": crontab(minute=0),  # Каждый час в :00
    },

    # Weekly digest — понедельник 9:00
    "weekly-digest": {
        "task": "workers.scheduled_tasks.generate_weekly_digest",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),
    },

    # TODO Phase 2: проверка почты каждые 5 минут
    # "check-mail": {
    #     "task": "workers.sync_tasks.check_mail",
    #     "schedule": 300.0,  # каждые 5 минут
    # },
}

"""
Конфигурация приложения.

Как это работает:
- pydantic-settings читает переменные окружения (из .env файла или системных)
- Каждое поле класса Settings = одна переменная окружения
- Типы проверяются автоматически: если POSTGRES_PORT=abc, будет ошибка при старте
- model_config задаёт откуда читать .env

Пример использования в коде:
    from src.core.config import settings
    print(settings.POSTGRES_HOST)  # -> "db" (из .env)
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Все настройки приложения в одном месте."""

    model_config = SettingsConfigDict(
        env_file=".env",           # Читаем из файла .env
        env_file_encoding="utf-8",
        extra="ignore",            # Игнорируем лишние переменные в .env
    )

    # --- App ---
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str = "change-me-in-production"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # --- Database ---
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "unified_ops"
    POSTGRES_USER: str = "dev"
    POSTGRES_PASSWORD: str = "dev_password_change_me"

    @property
    def database_url(self) -> str:
        """URL подключения к PostgreSQL через asyncpg (async драйвер)."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def database_url_sync(self) -> str:
        """Синхронный URL — нужен для Alembic (миграции не умеют async)."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Redis ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # --- Celery ---
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # --- S3 ---
    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "home-ai-os"
    S3_REGION: str = "ru-1"

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBHOOK_URL: str = ""

    # --- AI: Anthropic ---
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"

    # --- AI: Ollama ---
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"

    # --- AI: Whisper ---
    WHISPER_MODEL: str = "large-v3"
    WHISPER_DEVICE: str = "cpu"

    # --- Logging ---
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "console"  # "console" для dev, "json" для prod


@lru_cache()
def get_settings() -> Settings:
    """
    Синглтон настроек.
    lru_cache гарантирует что объект создаётся один раз.
    """
    return Settings()


# Удобный алиас — просто импортируй settings
settings = get_settings()

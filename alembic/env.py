"""
Alembic environment — связывает Alembic с нашими моделями и БД.

Этот файл вызывается при каждой команде alembic.
Он говорит Alembic:
1. Где взять URL базы данных (из нашего config.py)
2. Какие модели отслеживать (из нашего models.py)
3. Как применять миграции (online = к работающей БД)
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Импортируем наши модели — Alembic должен их "видеть"
# чтобы автоматически генерировать миграции
from src.core.database import Base
from src.core.models import (  # noqa: F401 — import нужен для регистрации моделей
    AIArtifact,
    AuditLog,
    Entity,
    EntityLink,
    EntityTag,
    InboxItem,
    Tag,
)
from src.core.config import settings

# Конфигурация Alembic из alembic.ini
config = context.config

# Подставляем URL БД из нашего config.py (синхронный драйвер для Alembic)
config.set_main_option("sqlalchemy.url", settings.database_url_sync)

# Настройка логирования из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata — Alembic сравнивает это с реальной БД
# и генерирует миграции на основе разницы
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Генерация SQL без подключения к БД.
    Используется редко: alembic upgrade head --sql > migration.sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Применение миграций к работающей БД.
    Это стандартный режим: alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

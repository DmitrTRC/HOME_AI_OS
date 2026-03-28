"""
Подключение к базе данных (SQLAlchemy 2.0 async).

Как это работает:
- create_async_engine — создаёт пул соединений к PostgreSQL
  (как connection pool в любом другом языке)
- async_sessionmaker — фабрика сессий (аналог "транзакции")
- В коде используем через dependency injection:
    async def get_db() -> AsyncSession:
        async with async_session() as session:
            yield session

Почему async:
- FastAPI — async фреймворк
- Один процесс может обрабатывать много запросов одновременно
- Не блокируемся на ожидании ответа от PostgreSQL
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

# Engine — пул соединений к БД
# echo=True в dev-режиме покажет все SQL-запросы в логах
engine = create_async_engine(
    settings.database_url,
    echo=settings.APP_DEBUG,
    pool_size=5,         # Сколько соединений держать открытыми
    max_overflow=10,     # Сколько ещё можно открыть при пиковой нагрузке
)

# Фабрика сессий
# expire_on_commit=False — объекты не "протухают" после commit
# (иначе любое обращение к полю после commit делало бы новый запрос в БД)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей.

    В SQLAlchemy 2.0 все модели наследуются от DeclarativeBase.
    Это аналог того, как в Django все модели наследуют models.Model.

    Пример:
        class Note(Base):
            __tablename__ = "notes"
            id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
            title: Mapped[str] = mapped_column(String(200))
    """
    pass


async def get_db() -> AsyncSession:
    """
    Dependency для FastAPI — даёт сессию БД в обработчик запроса.

    Использование в route:
        @router.get("/notes")
        async def list_notes(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Note))
            return result.scalars().all()

    yield — значит сессия автоматически закроется после обработки запроса.
    """
    async with async_session() as session:
        yield session

"""
Главный файл FastAPI-приложения.

FastAPI — это современный async web-фреймворк для Python.
Аналогия: как Express.js для Node.js, но с автодокументацией.

При запуске (uvicorn src.web.app:app):
1. Создаётся экземпляр FastAPI
2. Подключаются роутеры (наборы эндпоинтов)
3. Запускаются startup-события (подключение к БД, S3)
4. Сервер начинает слушать HTTP-запросы

Документация API автоматически доступна:
- http://localhost:8000/docs — Swagger UI (интерактивная)
- http://localhost:8000/redoc — ReDoc (читаемая)
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.core.logging import setup_logging
from src.core.storage import StorageService
from src.web.routes import health

# Путь к шаблонам Jinja2
TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle приложения.

    Код ДО yield — выполняется при старте (как __init__).
    Код ПОСЛЕ yield — выполняется при остановке (как __del__).
    """
    # === STARTUP ===
    setup_logging()
    logger.info(
        "app_starting",
        env=settings.APP_ENV,
        debug=settings.APP_DEBUG,
    )

    # Проверяем/создаём S3 bucket
    try:
        storage = StorageService()
        storage.ensure_bucket()
    except Exception as e:
        logger.warning("s3_init_warning", error=str(e), hint="MinIO may not be running")

    logger.info("app_started", port=settings.APP_PORT)

    yield  # Приложение работает

    # === SHUTDOWN ===
    logger.info("app_stopping")


# Создаём приложение
app = FastAPI(
    title="HOME AI OS",
    description="Unified Personal / Family / Project Operations System",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.APP_DEBUG else None,      # Swagger только в dev
    redoc_url="/redoc" if settings.APP_DEBUG else None,     # ReDoc только в dev
)


# --- Подключаем роутеры (группы эндпоинтов) ---
# Каждый домен будет добавлять свой роутер по мере реализации

# Системные эндпоинты (health check, info)
app.include_router(health.router, prefix="/api/v1", tags=["system"])

# TODO Phase 1: knowledge router
# TODO Phase 1: tasks router
# TODO Phase 1: intake router
# TODO Phase 2: documents router
# TODO Phase 2: media router
# TODO Phase 2: search router
# TODO Phase 3: medical router
# TODO Phase 3: registry router
# TODO Phase 4: operations router
# TODO Phase 4: reports router


# --- Главная страница ---
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница — dashboard."""
    return templates.TemplateResponse("index.html", {"request": request})

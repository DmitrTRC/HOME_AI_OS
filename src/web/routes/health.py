"""
Health check и системная информация.

Health check — стандартный паттерн: эндпоинт /health
который отвечает "я жив" (или "я болен").

Используется:
- Docker healthcheck
- Мониторинг (Prometheus, Uptime Kuma)
- Load balancer (если будет)
- Просто проверить что всё работает: curl localhost:8000/api/v1/health
"""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from src.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Ответ health check."""
    status: str
    version: str
    environment: str
    timestamp: str


class InfoResponse(BaseModel):
    """Информация о системе."""
    name: str
    version: str
    environment: str
    description: str
    domains: list[str]


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Проверка работоспособности.

    Возвращает статус приложения. В будущем будет проверять
    подключение к БД, Redis, S3.
    """
    return HealthResponse(
        status="ok",
        version="0.1.0",
        environment=settings.APP_ENV,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/info", response_model=InfoResponse)
async def system_info():
    """Общая информация о системе и доступных доменах."""
    return InfoResponse(
        name="HOME AI OS",
        version="0.1.0",
        environment=settings.APP_ENV,
        description="Unified Personal / Family / Project Operations System",
        domains=[
            "knowledge",
            "tasks",
            "medical",
            "vehicles",
            "registry",
            "operations",
            "creative",
            "dev",
            "documents",
            "media",
            "reports",
            "search",
        ],
    )

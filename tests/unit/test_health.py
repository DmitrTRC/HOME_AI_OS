"""
Тесты health check.

Первый тест в проекте — проверяет что приложение стартует
и отвечает на базовые запросы.

Запуск:
    pytest tests/unit/test_health.py -v
    pytest  # запустить все тесты
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.web.app import app


@pytest.mark.asyncio
async def test_health_returns_ok():
    """GET /api/v1/health должен вернуть status=ok."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_info_returns_domains():
    """GET /api/v1/info должен вернуть список доменов."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/info")

    assert response.status_code == 200
    data = response.json()
    assert "knowledge" in data["domains"]
    assert "medical" in data["domains"]
    assert "tasks" in data["domains"]

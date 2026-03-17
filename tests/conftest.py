"""
Конфигурация pytest.

conftest.py — специальный файл pytest.
Фикстуры (fixtures) объявленные здесь доступны ВСЕМ тестам.

Фикстура — это подготовка среды для теста.
Аналог setUp/tearDown из unittest, но удобнее.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.web.app import app


@pytest.fixture
def anyio_backend():
    """Используем asyncio (не trio)."""
    return "asyncio"


@pytest.fixture
async def client():
    """
    HTTP-клиент для тестирования API.

    Вместо реального HTTP-запроса — вызывает FastAPI напрямую.
    Быстро и не нужен запущенный сервер.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

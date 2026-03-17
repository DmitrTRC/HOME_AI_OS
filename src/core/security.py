"""
Безопасность, авторизация и аудит.

Phase 0: базовая структура.
- JWT токены для веб-интерфейса
- Проверка Telegram user по ID
- Запись в audit log

Зачем JWT:
В HTTP нет "сессий" — каждый запрос независимый.
JWT (JSON Web Token) — подписанный токен который клиент
отправляет с каждым запросом. Сервер проверяет подпись
и знает кто обращается. Как cookie с подписью.
"""

import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
import structlog

from src.core.config import settings

logger = structlog.get_logger()

# Алгоритм подписи JWT
ALGORITHM = "HS256"
# Время жизни токена — 24 часа
ACCESS_TOKEN_EXPIRE_HOURS = 24


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Создать JWT токен.

    Args:
        data: Данные для кодирования (обычно {"sub": user_id})
        expires_delta: Время жизни (по умолчанию 24 часа)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    """
    Проверить JWT токен. Вернуть payload или None если невалидный.
    """
    try:
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def write_audit_log(
    db_session,
    *,
    entity_id: uuid.UUID | None = None,
    actor_id: str | None = None,
    actor_type: str = "user",
    action: str,
    details: dict | None = None,
    ip_address: str | None = None,
) -> None:
    """
    Записать событие в audit log.

    Вызывается при любом значимом действии:
    - Создание/изменение/удаление сущности
    - AI-обработка
    - Экспорт данных
    - Доступ к чувствительным данным
    """
    from src.core.models import AuditLog

    log_entry = AuditLog(
        entity_id=entity_id,
        actor_id=actor_id,
        actor_type=actor_type,
        action=action,
        details=details,
        ip_address=ip_address,
    )
    db_session.add(log_entry)
    await db_session.flush()

    logger.info(
        "audit_logged",
        action=action,
        entity_id=str(entity_id) if entity_id else None,
        actor=actor_id,
    )

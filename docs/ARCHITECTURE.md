# Architecture Vision & Technology Stack

> Полный документ с детальным стеком: был создан в первом сообщении этого чата  
> и доступен как `architecture_vision.md` в файлах чата.

## Краткая сводка

### Архитектура: Modular Monolith
Одно приложение, но каждый домен — изолированный Python-пакет.
Не микросервисы. Вынос в отдельные сервисы — позже, если понадобится.

### Стек

| Слой | Технология |
|------|-----------|
| Язык | Python 3.12+ |
| Web | FastAPI + uvicorn |
| Bot | aiogram 3 (Telegram) |
| Queue | Celery 5 + Redis 7 |
| ORM | SQLAlchemy 2.0 async + Alembic |
| DB | PostgreSQL 16 + pgvector |
| Storage | S3 (MinIO dev / Selectel prod) |
| AI Cloud | Anthropic Claude API |
| AI Local | Ollama (Qwen2.5 / Mistral) |
| Speech | faster-whisper |
| OCR | Tesseract 5 + EasyOCR |
| Frontend | Jinja2 + HTMX + Alpine.js |
| Containers | Docker + Docker Compose |
| Hosting | Selectel Cloud (RU Zone) |

### Ключевые ADR

| # | Решение | Обратимость |
|---|---------|-------------|
| ADR-001 | Python + FastAPI | Средняя |
| ADR-002 | Modular Monolith | Высокая |
| ADR-003 | PostgreSQL + pgvector | Высокая |
| ADR-004 | HTMX вместо SPA | Высокая |
| ADR-005 | Celery + Redis | Средняя |
| ADR-006 | Ollama для sensitive data | Высокая |
| ADR-007 | Entity table + JSONB | Средняя |
| ADR-008 | aiogram 3 | Средняя |

### Phased Delivery

| Phase | Срок | Что |
|-------|------|-----|
| 0 | 2-3 нед | Foundation: Docker, DB, API, CI |
| 1 | 3-4 нед | Telegram bot + Knowledge + Tasks |
| 2 | 3-4 нед | Documents + Media + Search |
| 3 | 3-4 нед | Medical + Vehicles + Registry |
| 4 | 3-4 нед | Operations + Reports |
| 5 | 2-3 нед | Creative + Dev + Polish |

### Selectel Infrastructure (prod)

| Сервис | Spec | ~₽/мес |
|--------|------|--------|
| VDS | 4 vCPU, 8 GB RAM | 3 000 |
| Managed PG | 2 vCPU, 4 GB RAM | 3 500 |
| Managed Redis | 1 GB | 1 000 |
| S3 | 50 GB | 150 |
| GPU (on-demand) | 10h/month | 2 000 |
| **Итого** | | **~9 650** |

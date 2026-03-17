# CLAUDE.md — Project Instructions for Claude Code

## Project: Unified Personal / Family / Project Operations System (HOME AI OS)

### What is this project?
A modular personal/family/project operations system that unifies:
- Knowledge base (notes, research, ideas)
- Data capture from Telegram, mail, file uploads
- Domain registries (medical, vehicles, inventory, collections)
- Operational logs (SAR, DND MAX patrols)
- Task/Kanban management
- Reports and analytics
- AI-assisted processing (classification, summarization, entity extraction, transcription)

### Tech Stack
- **Language:** Python 3.12+
- **Web Framework:** FastAPI (async, Pydantic v2, OpenAPI)
- **Bot:** aiogram 3 (Telegram)
- **Task Queue:** Celery 5 + Redis
- **ORM:** SQLAlchemy 2.0 (async) + Alembic (migrations)
- **Database:** PostgreSQL 16 + pgvector extension
- **Cache/Broker:** Redis 7
- **Object Storage:** S3-compatible (Selectel S3 in prod, MinIO in dev)
- **AI:** Anthropic Claude API (primary), Ollama (local/sensitive), faster-whisper (transcription)
- **OCR:** Tesseract 5 + EasyOCR
- **Frontend:** FastAPI + Jinja2 + HTMX + Alpine.js (server-side rendering, no SPA)
- **Containers:** Docker + Docker Compose
- **Prod Hosting:** Selectel Cloud (RU Zone)

### Architecture: Modular Monolith
Each domain is a separate Python package under `src/`. Modules communicate through:
- Direct service calls (within same process)
- Domain events (in-process event bus)
- Celery tasks (async/heavy processing)

**NOT microservices.** One deployable unit. Extract to services later if needed.

### Project Structure
```
src/
├── core/           # Shared kernel: config, DB, auth, AI abstraction, storage
│   └── ai/         # AI provider abstraction layer
├── intake/         # Capture subsystem: Telegram bot, mail, file upload
│   └── adapters/   # Channel-specific adapters
├── knowledge/      # Notes, ideas, research, summaries
├── tasks/          # Kanban, epics, checklists, decisions, risks
├── medical/        # Medical records (high sensitivity)
├── registry/       # Vehicles, inventory, coins, regulated items
├── operations/     # SAR, DND MAX, field logs
├── creative/       # Sound studio, audiophile rack
├── dev/            # Dev projects, decisions, changelogs
├── documents/      # PDF/DOCX processing, office integrations
├── media/          # Photo/video/audio processing
├── reports/        # Report generation, digests, dashboards
├── search/         # Global search (FTS + semantic)
└── web/            # FastAPI app, routes, templates
workers/            # Celery workers and beat schedules
alembic/            # Database migrations
tests/              # Unit, integration, e2e tests
docs/               # Project documentation
scripts/            # CLI utilities, maintenance scripts
```

### Key Conventions

#### Python
- Python 3.12+, use type hints everywhere
- Async by default (async def, await)
- Pydantic v2 for all schemas (input/output validation)
- SQLAlchemy 2.0 style (mapped_column, DeclarativeBase)
- One module = one domain. Cross-domain calls go through service interfaces
- AI results are ALWAYS stored separately from source data (ai_artifacts table)

#### Naming
- Files: snake_case.py
- Classes: PascalCase
- Functions/variables: snake_case
- Constants: UPPER_SNAKE_CASE
- DB tables: snake_case, plural (entities, tasks, inbox_items)
- API routes: /api/v1/{domain}/{resource}

#### Database
- All models inherit from `src.core.models.Base`
- Use `TimestampMixin` for created_at/updated_at
- Use `AuditMixin` for sensitive entities
- Migrations via Alembic: `alembic revision --autogenerate -m "description"`
- JSONB for flexible domain-specific fields (`meta` column)
- pgvector for embeddings (`embedding` column)

#### Testing
- pytest + pytest-asyncio
- Tests mirror src/ structure: tests/unit/knowledge/test_service.py
- Use factories (factory_boy) for test data
- Integration tests use test database (docker)

#### Docker
- `docker compose up` — starts everything for dev
- `docker compose -f docker-compose.prod.yml up` — production config
- Services: app, bot, worker, beat, db, redis

#### Environment
- `.env` for local secrets (NEVER commit)
- `.env.example` as template
- `src/core/config.py` loads all settings via pydantic-settings

### Working with this project in Claude Code

When asked to implement a feature:
1. Check if the domain module exists in src/
2. If creating new module: models.py → schemas.py → service.py → routes
3. Write migration: `alembic revision --autogenerate -m "add X"`
4. Write tests alongside implementation
5. Update this CLAUDE.md if architecture changes

When asked to debug:
1. Check logs: `docker compose logs -f <service>`
2. Check DB: `docker compose exec db psql -U dev unified_ops`
3. Check Redis: `docker compose exec redis redis-cli`

### Sensitivity Levels
- 0 = normal (notes, tasks, general)
- 1 = internal (dev projects, work)
- 2 = sensitive (financial, personal)
- 3 = restricted (medical, regulated items)

Level 2+ data uses local AI (Ollama) instead of cloud APIs.

### Language
- Code: English (variables, comments, docstrings)
- UI text: Russian (user-facing strings)
- Documentation: Russian (primary) + English (code docs)
- Commit messages: English

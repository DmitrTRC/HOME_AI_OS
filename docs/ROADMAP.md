# 🗺 Development Roadmap

<p align="center">
  <img src="https://img.shields.io/badge/Total_Phases-6-blue?style=for-the-badge" alt="Phases">
  <img src="https://img.shields.io/badge/Timeline-4--5_months-green?style=for-the-badge" alt="Timeline">
  <img src="https://img.shields.io/badge/Current-Phase_0_✅-success?style=for-the-badge" alt="Current">
</p>

---

## 📊 Overview

```
 2026
 Mar          Apr          May          Jun          Jul          Aug
 ├────────────┼────────────┼────────────┼────────────┼────────────┤
 │▓▓▓▓▓▓▓▓▓▓▓│░░░░░░░░░░░░░░░░░░░░░░░░│            │            │
 │  Phase 0   │       Phase 1           │            │            │
 │ Foundation │ Telegram+Knowledge+Tasks│            │            │
 │    ✅      │         ⏳              │            │            │
 │            │            │░░░░░░░░░░░░░░░░░░░░░░░░░│            │
 │            │            │       Phase 2           │            │
 │            │            │  Docs+Media+Search      │            │
 │            │            │            │░░░░░░░░░░░░░░░░░░░░░░░░░│
 │            │            │            │       Phase 3           │
 │            │            │            │ Medical+Vehicles+Registry│
 │            │            │            │            │░░░░░░░░░░░░│
 │            │            │            │            │  Phase 4-5 │
 │            │            │            │            │ Ops+Reports│
 ├────────────┼────────────┼────────────┼────────────┼────────────┤
                                                         MVP ────►│
```

---


## ✅ Phase 0 — Foundation (2-3 недели)

> **Статус:** ✅ Завершена  
> **Цель:** Скелет проекта, базовые абстракции, dev-окружение

<details>
<summary><b>📋 Checklist (click to expand)</b></summary>

- [x] Репозиторий GitHub
- [x] CLAUDE.md для Claude Code
- [x] Docker Compose: app, bot, worker, beat, db, redis, minio
- [x] Dockerfile с системными зависимостями (ffmpeg, tesseract)
- [x] FastAPI skeleton + health check endpoint
- [x] PostgreSQL 16 + pgvector + pg_trgm расширения
- [x] SQLAlchemy 2.0 async models (Entity, AIArtifact, AuditLog, InboxItem)
- [x] Alembic migrations setup
- [x] Celery + Redis: worker + beat + scheduled tasks
- [x] AI Provider abstraction (Protocol + Router)
- [x] Claude API provider
- [x] Ollama provider (local AI)
- [x] S3 storage abstraction (MinIO/Selectel)
- [x] JWT auth & audit log
- [x] Structured logging (structlog)
- [x] Telegram bot skeleton (/start, /status, /help)
- [x] Jinja2 + HTMX base template
- [x] Unit tests + conftest
- [x] GitHub Actions CI pipeline
- [x] Makefile with developer commands
- [x] Documentation: README, Getting Started, Architecture, Glossary

</details>

### 📦 Deliverables
| Artifact | Status |
|----------|:------:|
| Docker dev environment | ✅ |
| FastAPI + health check | ✅ |
| PostgreSQL + pgvector schema | ✅ |
| AI Provider abstraction | ✅ |
| Telegram bot skeleton | ✅ |
| CI pipeline | ✅ |
| Project documentation | ✅ |

---


## 🔄 Phase 1 — Capture + Knowledge + Tasks (3-4 недели)

> **Статус:** 🔄 Следующая  
> **Цель:** Telegram intake работает, заметки и задачи создаются через AI  
> **MVP Milestone:** После Phase 1 система уже полезна!

### 🎯 Key Features

| Feature | Description | Priority |
|---------|------------|:--------:|
| 📱 **Telegram Intake** | Приём текста, голосовых, фото, документов | 🔴 P0 |
| 🎤 **Voice → Text** | Whisper транскрибация голосовых | 🔴 P0 |
| 🧠 **AI Classification** | Автоопределение домена и типа | 🔴 P0 |
| 📝 **Knowledge CRUD** | Создание, поиск, редактирование заметок | 🔴 P0 |
| ✅ **Task Kanban** | Доска задач с базовыми статусами | 🔴 P0 |
| 🔍 **FTS Search** | Полнотекстовый поиск (PostgreSQL) | 🟡 P1 |
| 🌐 **Web UI: Inbox** | Просмотр и ручная классификация входящих | 🟡 P1 |
| 🌐 **Web UI: Notes** | Список заметок + просмотр | 🟡 P1 |
| 🌐 **Web UI: Kanban** | Доска задач (HTMX + Sortable.js) | 🟡 P1 |
| 📱 **Telegram Commands** | /note, /task, /search, /inbox | 🟡 P1 |
| 📥 **Free-form Capture** | Отправляешь что угодно — AI разбирает | 🟢 P2 |

### 📋 Technical Tasks

<details>
<summary><b>Click to expand</b></summary>

- [ ] aiogram 3 handlers: text, voice, photo, document, video
- [ ] Download media from Telegram → upload to S3
- [ ] Whisper integration (faster-whisper): OGG → WAV → text
- [ ] AI classification pipeline: text → ClassifyResult → route to domain
- [ ] Entity extraction from text
- [ ] Knowledge module: models, schemas, service, routes
- [ ] Tasks module: models, schemas, service, kanban logic
- [ ] Inbox review page (HTMX)
- [ ] Notes list + detail page
- [ ] Kanban board (HTMX + Sortable.js drag-and-drop)
- [ ] Telegram command handlers (/note, /task, /search)
- [ ] Celery task: process_inbox_item (full implementation)
- [ ] Auto-summarization for long texts
- [ ] PostgreSQL FTS indexing (GIN + tsvector Russian/English)
- [ ] Integration tests

</details>

---


## ⏳ Phase 2 — Documents + Media + Search (3-4 недели)

> **Цель:** Полноценный media pipeline, обработка документов, глобальный семантический поиск

| Feature | Description |
|---------|------------|
| 📄 **Document Processing** | PDF text extraction, DOCX parsing, XLSX reading |
| 🖼 **Photo Pipeline** | OCR (Tesseract + EasyOCR), AI description, entity extraction |
| 🎬 **Video Pipeline** | Audio extraction → Whisper, key frame extraction |
| 🎤 **Audio Pipeline** | Full transcription with timestamps |
| 🔍 **Semantic Search** | Embeddings (multilingual-e5) + pgvector similarity search |
| 🌐 **Global Search UI** | Поиск по всем доменам с фильтрами |
| 📧 **Mail Intake** | IMAP adapter: письма → InboxItem → classification |
| 🔗 **Entity Linking** | UI для связывания сущностей между доменами |
| 📎 **Deduplication** | Обнаружение дубликатов media/documents |

---

## ⏳ Phase 3 — Domain Registries (3-4 недели)

> **Цель:** Доменные реестры для повседневной жизни

| Feature | Description |
|---------|------------|
| 🏥 **Medical Module** | Люди + животные, визиты, анализы, timeline, reminders |
| 🚗 **Vehicles Module** | ТС, страховки, сервис, расходы, напоминания |
| 📸 **A/V/Photo Inventory** | Техника, серийные номера, гарантии, фото |
| 🪙 **Coin Collection** | Каталог, атрибуты, оценки, confidence |
| 🔒 **Regulated Items** | Документы, сроки, разрешения, аудит |
| ⏰ **Reminder Engine** | Cross-domain напоминания → Telegram notifications |
| 🔐 **Access Control** | Sensitivity-based routing (restricted → local AI only) |
| 🌐 **Domain Views** | Специализированные UI для каждого реестра |

---

## ⏳ Phase 4 — Operations + Reports (3-4 недели)

> **Цель:** Полевые операции, отчёты и аналитика

| Feature | Description |
|---------|------------|
| 🏔 **SAR Module** | Missions, incidents, participants, evidence, timeline |
| 🛡 **DND MAX Module** | Patrols, shifts, events, incident logs |
| 📝 **Quick Field Entry** | Telegram: фото + голос → автопривязка к patrol/mission |
| 📊 **Report Builder** | draft → review → finalize workflow |
| 📅 **Weekly Digest** | Автоматический weekly/monthly обзор |
| 📈 **Dashboard** | Обзорные графики (HTMX + Chart.js) |
| 📤 **Export** | PDF, DOCX, JSON экспорт отчётов |
| 🔄 **Report Templates** | Шаблоны по доменам (SAR, DND, medical, inventory) |

---

## ⏳ Phase 5 — Creative + Dev + Polish (2-3 недели)

> **Цель:** Оставшиеся домены, стабилизация, подготовка к prod

| Feature | Description |
|---------|------------|
| 🎵 **Sound Studio** | Creative projects, sessions, references, equipment links |
| 🎧 **Audiophile Rack** | Components, configurations, listening notes, history |
| 📡 **RF Monitoring** | Sessions, observations, anomalies, reports |
| 💻 **Dev Branch** | Projects, decisions, changelog, reusable knowledge |
| 🌐 **Admin Panel** | User management, system settings, backup status |
| 🚀 **Prod Deploy** | Selectel: Managed PG + Redis + S3 + VDS |
| 📝 **Documentation** | Final docs, API reference, deployment guide |
| 🧪 **Load Testing** | Performance baseline |
| 🔒 **Security Audit** | Secrets rotation, access review |

---


## 🔮 Future (Post-MVP)

| Feature | When | Description |
|---------|------|-------------|
| 📱 PWA | v1.1 | Progressive Web App для мобильного доступа |
| 🤖 MAX Integration | v1.2 | Адаптер для MAX messenger (когда появится API) |
| 📊 Knowledge Graph | v1.3 | Neo4j для сложных связей между сущностями |
| 🔍 Advanced Analytics | v1.4 | Тренды, аномалии, предиктивные напоминания |
| 🌍 Multi-user | v2.0 | Полноценная multi-tenant система |
| 📦 Product Packaging | v3.0 | Коммерческая версия / SaaS |

---

## 📏 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Capture Speed** | < 3 actions to save anything | UX testing |
| **AI Accuracy** | > 80% correct domain classification | Confusion matrix on 100 samples |
| **Search Recall** | Find relevant content 90%+ of time | Manual testing over 2 weeks |
| **Uptime** | 99%+ on Selectel | Monitoring (Prometheus) |
| **Reminder Coverage** | 0 missed deadlines | Audit log review |

---

## 🏗 Architecture Evolution

```
Phase 0-1:  Monolith          Phase 2-3:  Modular Monolith     Phase 4+:    Extractable
┌─────────────┐               ┌─────────────┐                  ┌─────────────┐
│ ┌─────────┐ │               │ ┌─────────┐ │                  │ ┌─────────┐ │
│ │   All   │ │       →       │ │Module A │ │        →         │ │Service A│ ├──→ own DB
│ │  Code   │ │               │ ├─────────┤ │                  │ ├─────────┤ │
│ │  Here   │ │               │ │Module B │ │                  │ │Module B │ │
│ └─────────┘ │               │ ├─────────┤ │                  │ ├─────────┤ │
│     DB      │               │ │Module C │ │                  │ │Module C │ │
└─────────────┘               │ └─────────┘ │                  │ └─────────┘ │
                              │   Shared DB  │                  │   Shared DB │
                              └─────────────┘                  └─────────────┘
```

---

<p align="center">
  <sub>📅 Last updated: March 2026 | 📄 <a href="MVP.md">See also: MVP Definition</a></sub>
</p>

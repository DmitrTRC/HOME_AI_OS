<p align="center">
  <img src="docs/assets/logo.svg" width="120" alt="HOME AI OS Logo">
</p>

<h1 align="center">🏠 HOME AI OS</h1>

<p align="center">
  <strong>Unified Personal / Family / Project Operations System</strong><br>
  <em>Модульная AI-powered операционная система для управления жизнью, проектами и знаниями</em>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-features">Features</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="docs/GETTING_STARTED.md">Documentation</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Claude_API-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude">
  <img src="https://img.shields.io/badge/AI-Ollama_(local)-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/AI-Whisper_(STT)-74aa9c?style=for-the-badge&logo=openai&logoColor=white" alt="Whisper">
  <img src="https://img.shields.io/badge/hosting-Selectel_🇷🇺-4B8BBE?style=for-the-badge" alt="Selectel">
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/dmitrymorozov/HOME_AI_OS?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/status-Phase_0_Foundation-yellow?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/code_style-ruff-000000?style=flat-square" alt="Code Style">
</p>

---


## 💡 Что это?

**HOME AI OS** — это персональная операционная система, которая объединяет все аспекты жизни в единую управляемую платформу с AI-поддержкой.

> 📥 Отправь голосовое в Telegram → AI транскрибирует, классифицирует и создаст заметку, задачу или запись в нужном реестре. Автоматически.

<table>
<tr>
<td width="50%">

### 🧠 Проблема
- Данные разбросаны по 15+ сервисам
- Заметки, документы, фото — в разных местах
- Ничего не связано друг с другом
- Требует слишком много ручной дисциплины
- Нет единого "операционного слоя"

</td>
<td width="50%">

### ✨ Решение
- **Один вход** — Telegram, почта, веб, файлы
- **AI-классификация** — данные сами находят своё место
- **Связанные сущности** — всё связано со всем
- **Минимум действий** — отправил и забыл
- **20 доменов** — от заметок до медицины

</td>
</tr>
</table>

---

## 🏗 Architecture

```
                        ╔══════════════════════════════════╗
                        ║         INTAKE LAYER             ║
                        ║  📱 Telegram  📧 Mail  📁 Upload ║
                        ╚═══════════════╤══════════════════╝
                                        │
                        ╔═══════════════╧══════════════════╗
                        ║      🔀 GATEWAY / AI ROUTER      ║
                        ║   FastAPI + Celery + AI Classify  ║
                        ╚═══════╤══════════════════╤═══════╝
                                │                  │
                    ┌───────────┘                  └───────────┐
                    ▼                                          ▼
        ╔═══════════════════╗                    ╔════════════════════╗
        ║   ⚡ SYNC PATH    ║                    ║   🔄 ASYNC PATH    ║
        ║  CRUD, Search,    ║                    ║  AI Processing,    ║
        ║  Quick Operations ║                    ║  Transcription,    ║
        ╚════════╤══════════╝                    ║  OCR, Reports      ║
                 │                               ╚═════════╤══════════╝
                 └──────────────┬───────────────────────────┘
                                ▼
        ╔══════════════════════════════════════════════════════╗
        ║                 📦 DOMAIN MODULES                    ║
        ║                                                      ║
        ║  📝 Knowledge  ✅ Tasks    🏥 Medical   🚗 Vehicles  ║
        ║  📋 Registry   🔍 Search   📊 Reports   🎵 Creative  ║
        ║  💻 Dev        🏔 SAR      🛡 DND MAX   📡 RF Mon    ║
        ╚══════════════════════╤═══════════════════════════════╝
                               ▼
        ╔══════════════════════════════════════════════════════╗
        ║                  💾 DATA LAYER                       ║
        ║                                                      ║
        ║  🐘 PostgreSQL 16   📦 S3 Storage    ⚡ Redis 7     ║
        ║     + pgvector        (Selectel)       (cache/queue) ║
        ╚══════════════════════════════════════════════════════╝
```


### 🎯 Key Architecture Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Architecture | **Modular Monolith** | Простота деплоя, лёгкий вынос модулей позже |
| AI Strategy | **Cloud + Local** | Claude API для обычных данных, Ollama для чувствительных |
| Search | **PostgreSQL FTS + pgvector** | Одна БД для всего, семантический поиск из коробки |
| Frontend | **HTMX + Alpine.js** | Нулевой build step, серверный рендеринг |
| Queue | **Celery + Redis** | Зрелая экосистема, проверено годами |

---

## ✨ Features

<table>
<tr>
<td width="33%" valign="top">

### 📥 Smart Capture
- Telegram bot (текст, голос, фото, видео, документы)
- Email intake (IMAP)
- File upload (web)
- Free-form input — AI сам разберёт
- Минимум действий для фиксации

</td>
<td width="33%" valign="top">

### 🧠 AI-Powered
- Автоклассификация по доменам
- Извлечение сущностей из текста
- Транскрибация аудио (Whisper)
- OCR (Tesseract + EasyOCR)
- Суммаризация и черновики
- **Чувствительные данные → только локальный AI**

</td>
<td width="33%" valign="top">

### 🔗 Everything Connected
- Связи между любыми сущностями
- Глобальный поиск (FTS + семантический)
- Таймлайны по кейсам и людям
- Автоматические напоминания
- Weekly/monthly дайджесты

</td>
</tr>
</table>


### 📦 20 Domain Modules

| | Domain | Description | Sensitivity |
|---|--------|------------|:-----------:|
| 📝 | **Knowledge** | Заметки, идеи, исследования, summaries | 🟢 Normal |
| ✅ | **Tasks / Kanban** | Задачи, эпики, решения, риски, WIP-лимиты | 🟢 Normal |
| 📥 | **Capture & Inbox** | Единый буфер приёма из всех каналов | 🟢 Normal |
| 📄 | **Documents** | PDF, DOCX, Office, сканы, метаданные | 🟢 Normal |
| 📧 | **Mail Intake** | Письма, вложения, follow-up actions | 🟡 Internal |
| 🖼 | **Media Archive** | Фото, видео, аудио + AI-анализ | 🟢 Normal |
| 🏔 | **SAR** | Поисково-спасательные миссии, кейсы, отчёты | 🟡 Internal |
| 🛡 | **DND MAX** | Патрули, смены, инциденты, журналы | 🟡 Internal |
| 🎵 | **Sound Studio** | Творческие проекты, сессии, референсы | 🟢 Normal |
| 🎧 | **Audiophile Rack** | Компоненты, конфигурации, listening notes | 🟢 Normal |
| 📡 | **RF Monitoring** | Сессии наблюдения, аномалии, логи | 🟡 Internal |
| 🏥 | **Medical Records** | Люди + животные, визиты, анализы, назначения | 🔴 Restricted |
| 🔒 | **Regulated Items** | Документы, сроки, разрешения, аудит | 🔴 Restricted |
| 🚗 | **Vehicles** | ТС, страховки, сервис, расходы | 🟡 Internal |
| 📸 | **A/V/Photo Inventory** | Техника, серийники, гарантии | 🟢 Normal |
| 🪙 | **Coin Collection** | Каталог, атрибуты, оценки, фото | 🟢 Normal |
| 💻 | **Dev Branch** | Проекты, решения, changelog, learning | 🟢 Normal |
| 📊 | **Reports** | Отчёты, дайджесты, дашборды | 🟢 Normal |
| 🔍 | **Global Search** | FTS + семантический поиск по всем доменам | 🟢 Normal |
| ⚙️ | **Admin / Security** | Роли, аудит, политики, бэкапы | 🔴 Restricted |

> 🔴 **Restricted** домены используют только локальный AI (Ollama) — данные никогда не покидают сервер

---

## 🚀 Quick Start


```bash
# 1. Clone & configure
git clone https://github.com/your-username/HOME_AI_OS.git
cd HOME_AI_OS
cp .env.example .env
# Edit .env — add TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY

# 2. Launch everything
make up

# 3. Create database tables
make migrate

# 4. Verify
curl http://localhost:8000/api/v1/health
# → {"status": "ok", "version": "0.1.0"}
```

### 🌐 Available Services (Dev)

| Service | URL | Credentials |
|---------|-----|-------------|
| 🖥 **Web App** | http://localhost:8000 | — |
| 📖 **API Docs (Swagger)** | http://localhost:8000/docs | — |
| 📦 **MinIO Console (S3)** | http://localhost:9001 | minioadmin / minioadmin |
| 🐘 **PostgreSQL** | localhost:5432 | dev / dev_password_change_me |
| ⚡ **Redis** | localhost:6379 | — |

### 🛠 Developer Commands

```bash
make help         # 📋 Show all commands
make up           # 🚀 Start all services
make down         # 🛑 Stop all services
make logs         # 📜 Follow all logs
make logs-app     # 📜 Follow app logs only
make test         # 🧪 Run tests
make lint         # 🔍 Check code (ruff)
make format       # ✨ Auto-format code
make migrate      # 🗄  Apply DB migrations
make migration MSG="add X"  # 📝 Create new migration
make db-shell     # 🐘 PostgreSQL console
make redis-shell  # ⚡ Redis console
make shell        # 🐚 Bash inside app container
make clean        # ⚠️  Delete all data!
```

---


## 🔧 Tech Stack

<table>
<tr><td colspan="3" align="center"><h3>Backend</h3></td></tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" height="25"><br><sub>Python 3.12+</sub></td>
<td align="center"><img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" height="25"><br><sub>Web Framework</sub></td>
<td align="center"><img src="https://img.shields.io/badge/Celery-37814A?style=flat-square&logo=celery&logoColor=white" height="25"><br><sub>Task Queue</sub></td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" height="25"><br><sub>ORM (async)</sub></td>
<td align="center"><img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" height="25"><br><sub>Validation</sub></td>
<td align="center"><img src="https://img.shields.io/badge/aiogram_3-26A5E4?style=flat-square&logo=telegram&logoColor=white" height="25"><br><sub>Telegram Bot</sub></td>
</tr>

<tr><td colspan="3" align="center"><h3>Data</h3></td></tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/PostgreSQL_16-336791?style=flat-square&logo=postgresql&logoColor=white" height="25"><br><sub>Primary DB + FTS</sub></td>
<td align="center"><img src="https://img.shields.io/badge/pgvector-336791?style=flat-square&logo=postgresql&logoColor=white" height="25"><br><sub>Semantic Search</sub></td>
<td align="center"><img src="https://img.shields.io/badge/Redis_7-DC382D?style=flat-square&logo=redis&logoColor=white" height="25"><br><sub>Cache + Broker</sub></td>
</tr>

<tr><td colspan="3" align="center"><h3>AI</h3></td></tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Claude_API-D97757?style=flat-square&logo=anthropic&logoColor=white" height="25"><br><sub>Cloud LLM</sub></td>
<td align="center"><img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" height="25"><br><sub>Local LLM</sub></td>
<td align="center"><img src="https://img.shields.io/badge/Whisper-74aa9c?style=flat-square&logo=openai&logoColor=white" height="25"><br><sub>Speech-to-Text</sub></td>
</tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Tesseract_5-4285F4?style=flat-square&logo=google&logoColor=white" height="25"><br><sub>OCR</sub></td>
<td align="center"><img src="https://img.shields.io/badge/EasyOCR-FF6F00?style=flat-square" height="25"><br><sub>Neural OCR</sub></td>
<td align="center"><img src="https://img.shields.io/badge/sentence--transformers-FBBF24?style=flat-square" height="25"><br><sub>Embeddings</sub></td>
</tr>

<tr><td colspan="3" align="center"><h3>Infrastructure</h3></td></tr>
<tr>
<td align="center"><img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" height="25"><br><sub>Containers</sub></td>
<td align="center"><img src="https://img.shields.io/badge/Selectel-4B8BBE?style=flat-square" height="25"><br><sub>RU Cloud ☁️</sub></td>
<td align="center"><img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" height="25"><br><sub>CI/CD</sub></td>
</tr>
</table>

---


## 🗺 Roadmap

> 📄 Подробный roadmap: [docs/ROADMAP.md](docs/ROADMAP.md) • MVP-определение: [docs/MVP.md](docs/MVP.md)

```
Phase 0 ███████████████████████████████████████ ✅ Foundation
Phase 1 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ⏳ Telegram + Knowledge + Tasks
Phase 2 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    Documents + Media + Search
Phase 3 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    Medical + Vehicles + Registry
Phase 4 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    Operations + Reports
Phase 5 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    Creative + Dev + Polish
```

| Phase | Duration | Milestone | Status |
|:-----:|:--------:|-----------|:------:|
| **0** | 2-3 нед | 🏗 Foundation: Docker, DB, API skeleton, CI | ✅ Done |
| **1** | 3-4 нед | 📱 Telegram intake + Knowledge + Kanban | 🔄 Next |
| **2** | 3-4 нед | 📄 Documents + Media pipeline + Global Search | ⏳ |
| **3** | 3-4 нед | 🏥 Medical + Vehicles + Inventory + Collections | ⏳ |
| **4** | 3-4 нед | 🏔 SAR/DND Operations + Reports + Dashboards | ⏳ |
| **5** | 2-3 нед | 🎵 Creative + Dev branch + Stabilization | ⏳ |

---

## 📁 Project Structure

```
HOME_AI_OS/
├── 📄 CLAUDE.md              # ← Claude Code reads this first
├── 📄 README.md
├── 📄 Makefile               # Developer commands cheatsheet
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml     # 6 services: app, bot, worker, beat, db, redis
├── ⚙️ pyproject.toml          # Dependencies & tool config
├── 🔑 .env.example           # Environment template
│
├── 📂 src/                    # Source code
│   ├── 📂 core/               # 🔧 Shared kernel
│   │   ├── config.py          #    Settings (pydantic-settings)
│   │   ├── database.py        #    PostgreSQL async connection
│   │   ├── models.py          #    Entity, AIArtifact, AuditLog, InboxItem
│   │   ├── security.py        #    JWT, audit logging
│   │   ├── storage.py         #    S3 abstraction (MinIO/Selectel)
│   │   ├── logging.py         #    Structured logging (structlog)
│   │   └── 📂 ai/             # 🧠 AI orchestration
│   │       ├── router.py      #    Cloud vs Local routing
│   │       ├── schemas.py     #    AI request/response types
│   │       └── 📂 providers/  #    Claude, Ollama implementations
│   ├── 📂 intake/             # 📥 Data capture
│   │   └── 📂 adapters/       #    Telegram, Mail, Upload, MAX (future)
│   ├── 📂 knowledge/          # 📝 Notes, ideas, research
│   ├── 📂 tasks/              # ✅ Kanban, epics, decisions
│   ├── 📂 medical/            # 🏥 Medical records (restricted)
│   ├── 📂 registry/           # 📋 Vehicles, inventory, coins
│   ├── 📂 operations/         # 🏔 SAR, DND MAX, field logs
│   ├── 📂 creative/           # 🎵 Studio, Audiophile Rack
│   ├── 📂 dev/                # 💻 Dev projects, decisions
│   ├── 📂 documents/          # 📄 PDF, DOCX processing
│   ├── 📂 media/              # 🖼 Photo/video/audio
│   ├── 📂 reports/            # 📊 Reports, digests
│   ├── 📂 search/             # 🔍 Global search
│   └── 📂 web/                # 🌐 FastAPI + Jinja2 + HTMX
│       ├── app.py
│       ├── 📂 routes/
│       └── 📂 templates/
│
├── 📂 workers/                # ⚙️ Celery tasks
├── 📂 alembic/                # 🗄 DB migrations
├── 📂 tests/                  # 🧪 Unit + Integration
├── 📂 docs/                   # 📖 Documentation
└── 📂 scripts/                # 🔧 CLI utilities
```


---

## 💰 Infrastructure Cost (Selectel Prod)

| Service | Spec | Monthly |
|---------|------|--------:|
| 🖥 VDS | 4 vCPU, 8 GB RAM, 80 GB NVMe | ₽3 000 |
| 🐘 Managed PostgreSQL | 2 vCPU, 4 GB RAM, 50 GB SSD | ₽3 500 |
| ⚡ Managed Redis | 1 GB | ₽1 000 |
| 📦 S3 Object Storage | 50 GB | ₽150 |
| 🎮 GPU (on-demand) | ~10h/month for local AI | ₽2 000 |
| | **Total** | **~₽9 650** |

---

## 📖 Documentation

| Document | Description |
|----------|------------|
| [📋 CLAUDE.md](CLAUDE.md) | Instructions for Claude Code AI assistant |
| [🚀 Getting Started](docs/GETTING_STARTED.md) | Step-by-step launch guide |
| [🏗 Architecture](docs/ARCHITECTURE.md) | Architecture decisions & tech stack |
| [📖 Glossary](docs/GLOSSARY.md) | Term definitions for developers |
| [🗺 Roadmap](docs/ROADMAP.md) | Detailed development roadmap |
| [🎯 MVP Definition](docs/MVP.md) | Minimum Viable Product scope |

---

## 🤝 Contributing

This is a personal project, but contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ and ☕ using Python, FastAPI, and AI</sub><br>
  <sub>Hosted on 🇷🇺 Selectel Cloud</sub>
</p>

<p align="center">
  <a href="#-home-ai-os">⬆ Back to top</a>
</p>

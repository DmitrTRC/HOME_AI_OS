# 🎯 MVP Definition — HOME AI OS

<p align="center">
  <img src="https://img.shields.io/badge/MVP_Scope-Phase_0_+_Phase_1-blue?style=for-the-badge" alt="MVP Scope">
  <img src="https://img.shields.io/badge/Timeline-5--7_weeks-green?style=for-the-badge" alt="Timeline">
  <img src="https://img.shields.io/badge/Team-1_developer_+_AI-purple?style=for-the-badge" alt="Team">
</p>

---

## 📖 Что такое MVP

**Minimum Viable Product** — минимальный работающий продукт, который:
- ✅ Решает главную проблему (хаос данных → единая система)
- ✅ Приносит реальную пользу с первого дня
- ✅ Достаточно мал чтобы довести до конца
- ❌ НЕ содержит всех 20 доменов
- ❌ НЕ содержит сложных отчётов и аналитики
- ❌ НЕ требует prod-хостинга (работает локально)

---

## 🎯 MVP = Phase 0 + Phase 1

### Один абзац

> Пользователь отправляет в Telegram текст, голосовое или фото.
> Система принимает, транскрибирует/распознаёт, AI определяет домен,
> создаёт заметку или задачу. Пользователь видит результат в Telegram
> и на веб-доске. Может искать по всем записям.

---

## ✅ Что входит в MVP


### 📥 Capture (Вход)

| Канал | Что принимает | AI-обработка |
|-------|--------------|-------------|
| 📱 **Telegram** | Текст, голосовые, фото, документы | Транскрибация, OCR, классификация |
| 🌐 **Web Upload** | Файлы через HTTP | Классификация |

### 🧠 AI Pipeline

```
📱 Telegram Message
    │
    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Save       │────▶│  Transcribe  │────▶│  AI Classify    │
│  Original   │     │  (if voice)  │     │  (domain, type) │
│  to S3      │     │  Whisper     │     │  Claude/Ollama  │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                                    ┌──────────────┼──────────────┐
                                    ▼              ▼              ▼
                              ┌──────────┐  ┌──────────┐  ┌──────────┐
                              │  📝 Note │  │  ✅ Task │  │  💡 Idea │
                              │ (knowledge)│ │ (kanban) │  │(knowledge)│
                              └──────────┘  └──────────┘  └──────────┘
                                    │              │              │
                                    └──────────────┼──────────────┘
                                                   ▼
                                           ┌──────────────┐
                                           │ 📱 Notify    │
                                           │   user in    │
                                           │   Telegram   │
                                           └──────────────┘
```

### 📝 Knowledge Module

| Feature | Description |
|---------|------------|
| Создание заметок | Через Telegram, web UI, или AI из inbox |
| Типы | Note, Idea, Research item |
| Теги | Свободные теги + автоматические от AI |
| Связи | Связь заметка↔заметка, заметка↔задача |
| Поиск | Полнотекстовый (PostgreSQL FTS) |
| AI Summary | Автоматическое резюме длинных текстов |

### ✅ Tasks / Kanban

| Feature | Description |
|---------|------------|
| Доска | Inbox → Backlog → Next → In Progress → Done |
| Создание | Из Telegram (/task), web UI, или AI из inbox |
| Приоритет | Urgent, High, Normal, Low |
| Связи | Задача↔заметка, задача↔задача |
| Домены | Каждая задача привязана к домену |

### 🌐 Web UI

| Page | What it shows |
|------|--------------|
| **Dashboard** | Статус системы, последние записи |
| **Inbox** | Необработанные входящие + ручная классификация |
| **Notes** | Список заметок с поиском |
| **Kanban** | Drag-and-drop доска задач |

---


## ❌ Что НЕ входит в MVP

> Всё это будет позже. Не сейчас. Не отвлекаемся.

| Feature | Phase | Why Later |
|---------|:-----:|-----------|
| 📧 Mail intake | 2 | Telegram достаточно для старта |
| 📄 Document processing (PDF/DOCX) | 2 | Нужен для Phase 3 доменов |
| 🔍 Semantic search | 2 | FTS покрывает MVP |
| 🏥 Medical records | 3 | Требует повышенной безопасности |
| 🚗 Vehicles, inventory | 3 | Не критично для старта |
| 🪙 Collections | 3 | Не критично для старта |
| 🏔 SAR / DND operations | 4 | Сложные workflow |
| 📊 Reports & dashboards | 4 | Нужна накопленная база данных |
| 🎵 Creative / Rack | 5 | Нишевые домены |
| 💻 Dev branch | 5 | Можно использовать отдельные инструменты |
| 📱 PWA / mobile app | Future | Telegram = мобильный интерфейс |
| 🤖 MAX integration | Future | API ещё не доступен |
| 🚀 Selectel prod deploy | Phase 4-5 | Dev-окружения достаточно |

---

## ✅ MVP Acceptance Criteria

MVP считается готовым когда **ВСЕ** критерии выполнены:

### Функциональные

| # | Критерий | Как проверить |
|---|---------|---------------|
| AC-1 | 📱 Отправляю текст в Telegram → появляется заметка | Отправить "Идея: купить новый микрофон" |
| AC-2 | 🎤 Отправляю голосовое → транскрибируется → заметка | Записать 30 сек голосовое |
| AC-3 | 📷 Отправляю фото → OCR → заметка с текстом | Сфотографировать документ |
| AC-4 | ✅ /task купить молоко → задача на доске | Команда в Telegram |
| AC-5 | 🔍 /search молоко → находит задачу и заметки | Поиск по тексту |
| AC-6 | 🌐 Вижу inbox в web UI | Открыть localhost:8000 |
| AC-7 | 🌐 Вижу kanban board в web UI | Drag-and-drop работает |
| AC-8 | 🧠 AI правильно определяет домен в 80%+ случаев | 20 тестовых сообщений |

### Технические

| # | Критерий | Как проверить |
|---|---------|---------------|
| TC-1 | `docker compose up` поднимает всё | Одна команда, все сервисы up |
| TC-2 | Health check отвечает 200 | `curl /api/v1/health` |
| TC-3 | Тесты проходят | `make test` → 0 failures |
| TC-4 | AI-артефакты отделены от данных | Таблица ai_artifacts, поле provider |
| TC-5 | Оригинальные файлы сохраняются в S3 | Проверить MinIO console |
| TC-6 | Audit log записывается | Проверить таблицу audit_log |

---


## 📖 MVP User Stories

### Story 1: Быстрая заметка
```
Как пользователь,
я хочу отправить текст в Telegram и получить заметку в базе,
чтобы не терять мысли и идеи.

✅ Acceptance: текст → InboxItem → AI classify → Note created → Telegram confirmation
```

### Story 2: Голосовая → текст
```
Как пользователь,
я хочу отправить голосовое сообщение и получить текстовую заметку,
чтобы фиксировать мысли на ходу.

✅ Acceptance: voice → Whisper → transcription → Note → Telegram shows text
```

### Story 3: Быстрая задача
```
Как пользователь,
я хочу написать "/task купить молоко" и увидеть задачу на доске,
чтобы не забывать дела.

✅ Acceptance: /task command → Task in Inbox column → visible on Kanban board
```

### Story 4: Поиск
```
Как пользователь,
я хочу найти все записи про "микрофон",
чтобы собрать информацию по теме.

✅ Acceptance: /search микрофон → returns notes + tasks matching query
```

### Story 5: Обзор входящих
```
Как пользователь,
я хочу видеть все необработанные входящие в web UI,
чтобы вручную переклассифицировать неверно определённые.

✅ Acceptance: web page shows pending inbox items with reclassify controls
```

---

## 📐 MVP Architecture Scope

```
┌────────────────────────────────────────────────────┐
│                    MVP BOUNDARY                     │
│                                                     │
│  📱 Telegram ─── 📥 Inbox ─── 🧠 AI Classify      │
│                       │                             │
│              ┌────────┼────────┐                    │
│              ▼        ▼        ▼                    │
│           📝 Notes  ✅ Tasks  💡 Ideas              │
│              │        │        │                    │
│              └────────┼────────┘                    │
│                       ▼                             │
│               🔍 FTS Search                         │
│               🌐 Web UI (HTMX)                     │
│               📱 Telegram responses                 │
│                                                     │
│  ╔═══════════════════════════════╗                  │
│  ║ 🐘 PostgreSQL + ⚡ Redis      ║                  │
│  ║ 📦 S3 (MinIO) + 🧠 AI Layer ║                  │
│  ╚═══════════════════════════════╝                  │
└────────────────────────────────────────────────────┘
```

---

## 💡 Principle

> **"Make it work, make it right, make it fast."**
> — Kent Beck
>
> MVP = **"Make it work"**. Phase 2-5 = "Make it right". Future = "Make it fast".

---

<p align="center">
  <sub>📅 Created: March 2026 | 📄 <a href="ROADMAP.md">See also: Full Roadmap</a></sub>
</p>

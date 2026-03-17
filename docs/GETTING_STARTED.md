# Getting Started — Пошаговый запуск проекта

## Что тебе нужно перед стартом

### 1. Docker Desktop
Если ещё не установлен — скачай с https://www.docker.com/products/docker-desktop/

Docker Desktop включает в себя:
- **Docker Engine** — движок контейнеров
- **Docker Compose** — оркестратор нескольких контейнеров
- **GUI** — графический интерфейс для мониторинга

После установки проверь:
```bash
docker --version        # Docker version 27.x
docker compose version  # Docker Compose version v2.x
```

### 2. Telegram Bot Token
1. Открой Telegram, найди @BotFather
2. Отправь `/newbot`
3. Придумай имя (например "Home AI OS Bot")
4. Придумай username (например `home_ai_os_bot`)
5. BotFather даст тебе токен вида `123456789:ABCdefGHI...`
6. Сохрани его — он пойдёт в `.env`

### 3. Anthropic API Key (опционально для Phase 0)
1. Зарегистрируйся на https://console.anthropic.com/
2. Создай API key
3. Сохрани — пойдёт в `.env`

Без него система будет работать, но AI-функции будут недоступны до настройки Ollama.

---

## Шаг 1: Создать .env файл

```bash
cd /Users/dmitrymorozov/AI-Work/HOME_AI_OS
cp .env.example .env
```

Открой `.env` в любом редакторе и заполни:

```env
# Обязательно заменить:
APP_SECRET_KEY=тут-длинная-случайная-строка-32-символа-минимум
POSTGRES_PASSWORD=придумай-пароль-для-бд

# Когда будет токен бота:
TELEGRAM_BOT_TOKEN=токен-от-BotFather

# Когда будет ключ Anthropic:
ANTHROPIC_API_KEY=sk-ant-...
```

**Остальное пока можно не трогать** — дефолтные значения рассчитаны на dev.

---

## Шаг 2: Запустить Docker

```bash
# Собрать образы и запустить все сервисы
make up

# Или если make не работает:
docker compose up -d
```

**Первый запуск** займёт 5-10 минут — Docker скачает образы (~2 ГБ) и соберёт наш контейнер. Последующие запуски — секунды.

Проверить что всё поднялось:
```bash
docker compose ps
```

Должно быть 6 сервисов в статусе "Up" или "running".

---

## Шаг 3: Проверить что работает

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Должен ответить:
# {"status":"ok","version":"0.1.0","environment":"development",...}
```

Или просто открой в браузере:
- http://localhost:8000/docs — Swagger UI (интерактивная документация API)
- http://localhost:9001 — MinIO Console (логин: minioadmin / minioadmin)

---

## Шаг 4: Создать первую миграцию БД

```bash
make migrate
# Или: docker compose exec app alembic upgrade head
```

Это создаст все таблицы в PostgreSQL.

Проверить что таблицы созданы:
```bash
make db-shell
# В psql:
\dt
# Должны быть: entities, entity_links, tags, entity_tags, ai_artifacts, audit_log, inbox_items
\q
```

---

## Шаг 5: Запустить тесты

```bash
make test
# Или: docker compose exec app pytest -v
```

Должно быть 2 passed, 0 failed.

---

## Что дальше

Phase 0 завершена когда:
- [x] Docker Compose запускает все сервисы
- [x] FastAPI отвечает на /health
- [x] PostgreSQL с pgvector работает
- [x] Redis работает
- [x] MinIO (S3) работает
- [x] Alembic создаёт таблицы
- [x] Тесты проходят
- [x] CLAUDE.md готов для Claude Code

Следующий шаг — **Phase 1: Telegram bot + Knowledge module + Tasks**.

---

## Решение проблем

### Docker не стартует
```bash
# Проверить логи конкретного сервиса:
docker compose logs db      # PostgreSQL
docker compose logs redis   # Redis
docker compose logs app     # Приложение
```

### Порт уже занят
Если ошибка "port already in use":
```bash
# Посмотреть кто занял порт:
lsof -i :8000  # (или :5432, :6379)
# Убить процесс или поменять порт в docker-compose.yml
```

### Хочу начать с чистого листа
```bash
make clean  # УДАЛИТ ВСЕ ДАННЫЕ!
make up     # Поднять заново
make migrate  # Создать таблицы
```

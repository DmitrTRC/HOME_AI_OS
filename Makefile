# ============================================================
# HOME AI OS — Makefile
# ============================================================
# Шпаргалка по частым командам. Вместо длинных docker compose...
# пишешь make up, make logs, make test.
#
# Как работает: make <цель> → выполняется рецепт (команды ниже)
# ============================================================

# Определяем команду docker compose (v2 без дефиса, v1 с дефисом)
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

.PHONY: help up down logs test lint migrate shell db-shell redis-shell

# Показать справку (make без аргументов)
help:
	@echo ""
	@echo "  HOME AI OS — Команды разработки"
	@echo "  ================================"
	@echo ""
	@echo "  Запуск:"
	@echo "    make up          — запустить все сервисы"
	@echo "    make down        — остановить все сервисы"
	@echo "    make restart     — перезапустить"
	@echo "    make logs        — логи всех сервисов (follow)"
	@echo "    make logs-app    — логи только приложения"
	@echo "    make logs-bot    — логи только бота"
	@echo "    make logs-worker — логи только worker"
	@echo ""
	@echo "  Разработка:"
	@echo "    make test        — запустить тесты"
	@echo "    make lint        — проверить код (ruff)"
	@echo "    make format      — отформатировать код (ruff)"
	@echo "    make migrate     — применить миграции БД"
	@echo "    make migration   — создать новую миграцию"
	@echo ""
	@echo "  Доступ к сервисам:"
	@echo "    make shell       — bash внутри контейнера app"
	@echo "    make db-shell    — psql к PostgreSQL"
	@echo "    make redis-shell — redis-cli"
	@echo ""
	@echo "  Очистка:"
	@echo "    make clean       — остановить и удалить volumes (ОСТОРОЖНО!)"
	@echo ""

# --- Запуск ---

up:
	$(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "✓ Сервисы запущены:"
	@echo "  App:   http://localhost:8000"
	@echo "  Docs:  http://localhost:8000/docs"
	@echo "  MinIO: http://localhost:9001"
	@echo ""

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f

logs-app:
	$(DOCKER_COMPOSE) logs -f app

logs-bot:
	$(DOCKER_COMPOSE) logs -f bot

logs-worker:
	$(DOCKER_COMPOSE) logs -f worker

# --- Разработка ---

test:
	$(DOCKER_COMPOSE) exec app pytest -v

lint:
	$(DOCKER_COMPOSE) exec app ruff check src/ workers/ tests/

format:
	$(DOCKER_COMPOSE) exec app ruff format src/ workers/ tests/

# Применить все миграции к БД
migrate:
	$(DOCKER_COMPOSE) exec app alembic upgrade head

# Создать новую миграцию (передай сообщение через MSG=)
# Пример: make migration MSG="add notes table"
migration:
	$(DOCKER_COMPOSE) exec app alembic revision --autogenerate -m "$(MSG)"

# --- Доступ ---

shell:
	$(DOCKER_COMPOSE) exec app bash

db-shell:
	$(DOCKER_COMPOSE) exec db psql -U dev unified_ops

redis-shell:
	$(DOCKER_COMPOSE) exec redis redis-cli

# --- Очистка ---

# ВНИМАНИЕ: удаляет все данные из БД, Redis, MinIO!
clean:
	$(DOCKER_COMPOSE) down -v
	@echo "✓ Все volumes удалены"

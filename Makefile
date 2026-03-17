# ============================================================
# HOME AI OS — Makefile
# ============================================================
# Шпаргалка по частым командам. Вместо длинных docker compose...
# пишешь make up, make logs, make test.
#
# Как работает: make <цель> → выполняется рецепт (команды ниже)
# ============================================================

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
	docker compose up -d
	@echo ""
	@echo "✓ Сервисы запущены:"
	@echo "  App:   http://localhost:8000"
	@echo "  Docs:  http://localhost:8000/docs"
	@echo "  MinIO: http://localhost:9001"
	@echo ""

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

logs-app:
	docker compose logs -f app

logs-bot:
	docker compose logs -f bot

logs-worker:
	docker compose logs -f worker

# --- Разработка ---

test:
	docker compose exec app pytest -v

lint:
	docker compose exec app ruff check src/ workers/ tests/

format:
	docker compose exec app ruff format src/ workers/ tests/

# Применить все миграции к БД
migrate:
	docker compose exec app alembic upgrade head

# Создать новую миграцию (передай сообщение через MSG=)
# Пример: make migration MSG="add notes table"
migration:
	docker compose exec app alembic revision --autogenerate -m "$(MSG)"

# --- Доступ ---

shell:
	docker compose exec app bash

db-shell:
	docker compose exec db psql -U dev unified_ops

redis-shell:
	docker compose exec redis redis-cli

# --- Очистка ---

# ВНИМАНИЕ: удаляет все данные из БД, Redis, MinIO!
clean:
	docker compose down -v
	@echo "✓ Все volumes удалены"

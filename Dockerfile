# ============================================================
# HOME AI OS — Dockerfile
# ============================================================
# Это «рецепт» для создания контейнера с нашим приложением.
# Контейнер — это изолированная среда, как виртуальная машина,
# но легче и быстрее.
# ============================================================

# Базовый образ: Python 3.12 на Debian Bookworm (slim = минимальный)
FROM python:3.12-slim-bookworm AS base

# Ставим системные зависимости которые нужны для наших Python-пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Для PostgreSQL (asyncpg, psycopg2)
    libpq-dev \
    # Для Pillow (работа с изображениями)
    libjpeg62-turbo-dev libpng-dev \
    # Для Tesseract OCR
    tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng \
    # Для ffmpeg (конвертация аудио/видео из Telegram)
    ffmpeg \
    # Общие утилиты
    curl gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файл зависимостей отдельно (для кэширования Docker-слоёв)
# Если pyproject.toml не изменился — Docker не будет пересобирать этот слой
COPY pyproject.toml .

# Ставим Python-зависимости
RUN pip install --no-cache-dir -e ".[dev]"

# Копируем весь код приложения
COPY . .

# Порт на котором слушает FastAPI
EXPOSE 8000

# Команда по умолчанию: запускаем FastAPI через uvicorn
# uvicorn — это ASGI-сервер (как apache/nginx, но для Python async)
# --reload — автоперезагрузка при изменении файлов (только для dev!)
CMD ["uvicorn", "src.web.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

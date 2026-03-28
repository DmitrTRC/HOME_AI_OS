"""
Telegram Bot — адаптер для приёма данных из Telegram.

Phase 0: минимальный бот, который стартует и отвечает на /start.
Phase 1: полноценный intake — текст, голосовые, фото, документы.

aiogram 3 — async фреймворк для Telegram Bot API.
Работает в двух режимах:
- Polling (dev): бот сам спрашивает Telegram "есть новые сообщения?"
- Webhook (prod): Telegram сам присылает сообщения на наш URL

Запуск:
    python -m src.intake.adapters.telegram
"""

import asyncio
import sys

import structlog

from src.core.config import settings
from src.core.logging import setup_logging

logger = structlog.get_logger()


async def main():
    """Запуск Telegram бота в polling-режиме."""
    setup_logging()

    token = settings.TELEGRAM_BOT_TOKEN
    if not token or token == "your-telegram-bot-token-here":
        logger.warning(
            "telegram_bot_skipped",
            reason="TELEGRAM_BOT_TOKEN not configured in .env",
            hint="Get token from @BotFather and add to .env",
        )
        # Не падаем — просто ждём. Docker restart policy перезапустит.
        # Когда токен будет настроен — бот заработает после рестарта.
        logger.info("telegram_bot_waiting", message="Waiting for token configuration...")
        while True:
            await asyncio.sleep(60)

    try:
        from aiogram import Bot, Dispatcher, types
        from aiogram.enums import ParseMode
        from aiogram.filters import Command
    except ImportError:
        logger.error("aiogram_not_installed", hint="pip install aiogram")
        sys.exit(1)

    # Создаём бота и диспетчер
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # --- Обработчики ---

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        """Команда /start — приветствие."""
        await message.answer(
            "🏠 <b>HOME AI OS</b>\n\n"
            "Я — твоя персональная операционная система.\n"
            "Отправь мне текст, голосовое, фото или документ — "
            "я сохраню, классифицирую и помогу разобрать.\n\n"
            "Команды:\n"
            "/start — это сообщение\n"
            "/status — статус системы\n"
            "/help — помощь\n\n"
            "<i>Phase 0: бот запущен, intake — в Phase 1</i>"
        )

    @dp.message(Command("status"))
    async def cmd_status(message: types.Message):
        """Команда /status — статус системы."""
        await message.answer(
            "📊 <b>Статус системы</b>\n\n"
            "✅ Bot: online\n"
            "✅ Phase: 0 (Foundation)\n\n"
            "⏳ Phase 1: Telegram intake + Knowledge + Tasks"
        )

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        """Команда /help."""
        await message.answer(
            "📖 <b>Помощь</b>\n\n"
            "Сейчас бот в режиме Phase 0 — foundation.\n"
            "В Phase 1 можно будет:\n"
            "• Отправлять текст → заметка\n"
            "• Отправлять голосовое → транскрипция + заметка\n"
            "• Отправлять фото → OCR + инвентаризация\n"
            "• Отправлять документ → извлечение + классификация\n\n"
            "/note текст — быстрая заметка\n"
            "/task текст — быстрая задача\n"
            "/search запрос — поиск по базе"
        )

    @dp.message()
    async def catch_all(message: types.Message):
        """Все остальные сообщения — Phase 1 intake."""
        # Phase 0: просто подтверждаем получение
        content_type = message.content_type
        logger.info(
            "telegram_message_received",
            user_id=message.from_user.id,
            content_type=content_type,
            text_preview=message.text[:100] if message.text else None,
        )
        await message.answer(
            f"📥 Получено ({content_type}).\n"
            f"<i>Обработка входящих — в Phase 1.</i>"
        )

    # --- Запуск ---
    logger.info("telegram_bot_starting", mode="polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

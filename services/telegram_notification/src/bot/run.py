import asyncio
from logging import getLogger

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Update
from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider, setup_dishka

from src.event_processor import (
    EventHandlersProvider,
    EventProcessor,
    EventProcessorProvider,
)

from .handlers import start
from .provider import BotProvider
from .utils.logs import setup_logging

logger = getLogger("bot.run")


class DebugMiddleware(BaseMiddleware):
    """Логирует все входящие updates для отладки"""
    async def __call__(self, handler, event: Update, data):
        logger.info(f"📥 Incoming update: type={event.event_type}")
        
        # Логируем только message.text, если это message
        if hasattr(event, 'message') and event.message:
            logger.info(f"   message.text = {event.message.text!r}")
        
        return await handler(event, data)


async def _run():
    setup_logging()

    container = make_async_container(
        EventProcessorProvider(),
        EventHandlersProvider(),
        BotProvider(),
        AiogramProvider(),
    )

    bot = await container.get(Bot)
    dp = await container.get(Dispatcher)

    # Подключаем Dishka к aiogram
    setup_dishka(container, dp, auto_inject=True)

    # Подключаем middleware для отладки
    dp.update.middleware(DebugMiddleware())

    # Регистрируем роутеры
    dp.include_router(start.router)

    try:
        processor = await container.get(EventProcessor)
        await processor.start_consumers()

        logger.info("Starting bot polling...")
        await dp.start_polling(bot)

    finally:
        await container.close()


def run():
    asyncio.run(_run())


    # После добавления инстанса бота в контейнер
    # вот это нужно раскомментировать:
    #
    # bot = await container.get(Bot)
    # setup_dishka(container, bot, auto_inject=True)
    #
    # если это раскомментировать, то можно использовать фичи dishka
    # в aiogram: https://dishka.readthedocs.io/en/stable/integrations/aiogram.html

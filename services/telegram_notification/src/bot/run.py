import asyncio
from logging import getLogger

from aiogram import Bot, Dispatcher
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

    setup_dishka(container, dp, auto_inject=True)

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

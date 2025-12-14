import asyncio
from dishka import make_async_container
from aiogram import Bot  # noqa: F401
from dishka.integrations.aiogram import setup_dishka, AiogramProvider  # noqa: F401

from event_processor import (
    EventProcessorProvider,
    EventHandlersProvider,
    EventProcessor,
)
from .provider import BotProvider
from .utils.logs import setup_logging


async def _run():
    setup_logging()

    container = make_async_container(
        EventProcessorProvider(),
        EventHandlersProvider(),
        BotProvider(),
        AiogramProvider(),
    )

    # После добавления инстанса бота в контейнер
    # вот это нужно раскомментировать:
    #
    # bot = await container.get(Bot)
    # setup_dishka(container, bot, auto_inject=True)
    #
    # если это раскомментировать, то можно использовать фичи dishka
    # в aiogram: https://dishka.readthedocs.io/en/stable/integrations/aiogram.html

    try:
        processor = await container.get(EventProcessor)
        await processor.start_consumers()
        await asyncio.Future()  # Это убрать, тут должно быть dispatcher.start_polling()
    finally:
        await container.close()


def run():
    asyncio.run(_run())

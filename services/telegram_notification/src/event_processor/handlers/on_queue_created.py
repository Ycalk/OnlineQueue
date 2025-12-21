from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Queue
from .base import BaseEventHandler
from event_processor.events import QueueCreated


class OnQueueCreated(BaseEventHandler[QueueCreated]):
    @classmethod
    def event_type(cls) -> type[QueueCreated]:
        return QueueCreated

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_queue_created")

    async def __call__(self, event: QueueCreated) -> None:
        self.logger.info(f"Queue {event.queue_id} created by {event.owner_id}")

        queue = Queue(
            queue_id=event.queue_id, owner_id=event.owner_id, name=event.queue_name
        )
        self.session.add(queue)
        await self.session.commit()

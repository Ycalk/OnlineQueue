from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request, Queue
from .base import BaseEventHandler
from event_processor.events import RequestCreated


class OnRequestCreated(BaseEventHandler[RequestCreated]):
    @classmethod
    def event_type(cls) -> type[RequestCreated]:
        return RequestCreated

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_request_created")

    async def __call__(self, event: RequestCreated) -> None:
        self.logger.info(f"Request {event.request_id} created by {event.user_id}")

        request = Request(
            request_id=event.request_id,
            user_id=event.user_id,
            queue_id=event.queue_id,
            status="pending",
        )
        self.session.add(request)
        await self.session.commit()

        queue = await self.session.get(Queue, event.queue_id)

        user = await self.session.get(TelegramUser, event.user_id)
        if not user or user.telegram_id == 0:
            return

        try:
            queue_name = queue.name if queue else "Неизвестная очередь"
            message = f"📝 Новая заявка создана!\n\nОчередь: {queue_name}"
            await self.bot.send_message(user.telegram_id, message)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

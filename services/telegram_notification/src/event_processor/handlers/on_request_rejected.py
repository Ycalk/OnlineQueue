from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request, Queue
from .base import BaseEventHandler
from event_processor.events import RequestRejected


class OnRequestRejected(BaseEventHandler[RequestRejected]):
    @classmethod
    def event_type(cls) -> type[RequestRejected]:
        return RequestRejected

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_request_rejected")

    async def __call__(self, event: RequestRejected) -> None:
        self.logger.info(f"Request {event.request_id} rejected")

        request = await self.session.get(Request, event.request_id)
        if not request:
            return

        queue = await self.session.get(Queue, request.queue_id)
        user = await self.session.get(TelegramUser, request.user_id)
        if not user or user.telegram_id == 0:
            return

        try:
            queue_name = queue.name if queue else "Неизвестная очередь"
            message = f"❌ Твоя заявка отклонена\n\nОчередь: {queue_name}"
            await self.bot.send_message(user.telegram_id, message)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

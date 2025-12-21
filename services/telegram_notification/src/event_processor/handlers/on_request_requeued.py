from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request, Queue
from .base import BaseEventHandler
from event_processor.events import RequestRequeued


class OnRequestRequeued(BaseEventHandler[RequestRequeued]):
    @classmethod
    def event_type(cls) -> type[RequestRequeued]:
        return RequestRequeued

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_request_requeued")

    async def __call__(self, event: RequestRequeued) -> None:
        self.logger.info(f"Request {event.request_id} requeued")

        request = await self.session.get(Request, event.request_id)
        if not request:
            return

        request.status = "pending"
        await self.session.commit()

        user = await self.session.get(TelegramUser, request.user_id)

        queue = await self.session.get(Queue, request.queue_id)
        if not queue:
            return

        if not user:
            return

        try:
            message = f"🔄 Заявка возвращена в очередь\n\nОчередь: {queue.name}\nЦель визита: {request.purpose}"
            await self.bot.send_message(user.telegram_id, message)
            self.logger.info(f"Notification sent to {user.telegram_id}")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

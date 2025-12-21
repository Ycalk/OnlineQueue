from logging import getLogger
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser
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

        result = await self.session.execute(
            select(TelegramUser).where(TelegramUser.user_id == event.user_id)
        )
        user = result.scalar_one_or_none()

        if not user or user.telegram_id == 0:
            return

        try:
            message = f"🔄 Заявка возвращена в очередь\n\nID: {event.request_id}"
            await self.bot.send_message(user.telegram_id, message)
            self.logger.info(f"Notification sent to {user.telegram_id}")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

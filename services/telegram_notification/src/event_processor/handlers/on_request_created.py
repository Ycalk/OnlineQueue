from logging import getLogger
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser
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
        self.logger.info(
            f"Request {event.request_id} created by {event.user_id}"
        )

        # Найти telegram_id пользователя
        result = await self.session.execute(
            select(TelegramUser).where(TelegramUser.user_id == event.user_id)
        )
        user = result.scalar_one_or_none()

        if not user or user.telegram_id == 0:
            self.logger.warning(f"User {event.user_id} has no linked Telegram")
            return

        # Отправить уведомление
        try:
            message = (
                f"📝 Новая заявка создана!\n\n"
                f"ID заявки: {event.request_id}"
            )
            
            await self.bot.send_message(user.telegram_id, message)
            self.logger.info(f"Notification sent to telegram_id={user.telegram_id}")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}", exc_info=True)

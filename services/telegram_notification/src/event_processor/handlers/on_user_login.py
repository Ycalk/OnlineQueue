from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser
from .base import BaseEventHandler
from event_processor.events import UserLogin


class OnUserLogin(BaseEventHandler[UserLogin]):
    @classmethod
    def event_type(cls) -> type[UserLogin]:
        return UserLogin

    def __init__(self, session: AsyncSession, bot: Bot):
        self._session = session
        self._bot = bot
        self._logger = getLogger("event_handler.on_user_login")

    async def __call__(self, event: UserLogin) -> None:
        user = await self._session.get(TelegramUser, event.user_id)

        if not user or user.telegram_id == 0:
            return

        try:
            text = f"🔐 Вход в аккаунт\n\nEmail: {event.email}"
            await self._bot.send_message(user.telegram_id, text)
            self._logger.info(f"Login notification sent to {user.telegram_id}")
        except Exception as e:
            self._logger.error(f"Failed to send login notification: {e}")

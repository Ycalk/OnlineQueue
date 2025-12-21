from logging import getLogger

from aiogram import Bot
from sqlalchemy import select
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
        # Проверяем, есть ли привязка
        result = await self._session.execute(
            select(TelegramUser).where(
                TelegramUser.user_id == event.user_id,
                TelegramUser.telegram_id != 0,
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            return  # Не привязан — не уведомляем

        ip_info = f" с IP {event.ip_address}" if event.ip_address else ""
        text = f"🔐 Вход в аккаунт{ip_info}"

        try:
            await self._bot.send_message(user.telegram_id, text)
        except Exception as e:
            self._logger.error(f"Failed to send login notification: {e}")

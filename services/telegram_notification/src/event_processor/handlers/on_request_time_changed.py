from logging import getLogger
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request
from .base import BaseEventHandler
from event_processor.events import RequestTimeChanged


class OnRequestTimeChanged(BaseEventHandler[RequestTimeChanged]):
    @classmethod
    def event_type(cls) -> type[RequestTimeChanged]:
        return RequestTimeChanged

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_request_time_changed")

    async def __call__(self, event: RequestTimeChanged) -> None:
        self.logger.info(f"Request {event.request_id} time changed")

        # Получаем Request из базы
        result = await self.session.execute(
            select(Request).where(Request.request_id == event.request_id)
        )
        request = result.scalar_one_or_none()

        if not request:
            self.logger.warning(f"Request {event.request_id} not found")
            return

        # Получаем TelegramUser
        result = await self.session.execute(
            select(TelegramUser).where(TelegramUser.user_id == request.user_id)
        )
        user = result.scalar_one_or_none()

        if not user or user.telegram_id == 0:
            return

        try:
            message = (
                f"🔄 Время твоей записи изменено!\n\n"
                f"📅 Новая дата: {event.new_confirmed_date.strftime('%d.%m.%Y')}\n"
                f"🕐 Новое время: {event.new_confirmed_time_start.strftime('%H:%M')} - "
                f"{event.new_confirmed_time_end.strftime('%H:%M')}\n"
                f"ID: {event.request_id}"
            )
            await self.bot.send_message(user.telegram_id, message)
            self.logger.info(f"Notification sent to {user.telegram_id}")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

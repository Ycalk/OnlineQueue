from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request, Queue
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

        request = await self.session.get(Request, event.request_id)
        if not request:
            return

        queue = await self.session.get(Queue, request.queue_id)
        user = await self.session.get(TelegramUser, request.user_id)
        if not user or user.telegram_id == 0:
            return

        try:
            queue_name = queue.name if queue else "Неизвестная очередь"
            message = (
                f"🔄 Время вашей записи изменено!\n\n"
                f"Очередь: {queue_name}\n"
                f"📅 Новая дата: {event.new_confirmed_date.strftime('%d.%m.%Y')}\n"
                f"🕐 Новое время: {event.new_confirmed_time_start.strftime('%H:%M')} - "
                f"{event.new_confirmed_time_end.strftime('%H:%M')}"
            )
            await self.bot.send_message(user.telegram_id, message)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

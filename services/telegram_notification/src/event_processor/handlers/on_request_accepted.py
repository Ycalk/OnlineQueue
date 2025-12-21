from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request, Queue
from .base import BaseEventHandler
from event_processor.events import RequestAccepted


class OnRequestAccepted(BaseEventHandler[RequestAccepted]):
    @classmethod
    def event_type(cls) -> type[RequestAccepted]:
        return RequestAccepted

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_request_accepted")

    async def __call__(self, event: RequestAccepted) -> None:
        self.logger.info(f"Request {event.request_id} accepted")

        request = await self.session.get(Request, event.request_id)
        if not request:
            return
        request.status = "accepted"
        await self.session.commit()

        queue = await self.session.get(Queue, request.queue_id)
        user = await self.session.get(TelegramUser, request.user_id)
        if not user:
            return

        try:
            queue_name = queue.name if queue else "Неизвестная очередь"
            message = (
                f"✅ Ваша заявка принята!\n\n"
                f"Очередь: {queue_name}\n"
                f"📅 Дата: {event.confirmed_date.strftime('%d.%m.%Y')}\n"
                f"🕐 Время: {event.confirmed_time_start.strftime('%H:%M')} - "
                f"{event.confirmed_time_end.strftime('%H:%M')}"
            )
            await self.bot.send_message(user.telegram_id, message)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

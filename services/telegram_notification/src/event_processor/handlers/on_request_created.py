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
            purpose=event.purpose,
            preferred_date=event.preferred_date,
            preferred_time_start=event.preferred_time_start,
            preferred_time_end=event.preferred_time_end,
        )
        self.session.add(request)
        await self.session.commit()

        queue = await self.session.get(Queue, event.queue_id)

        if queue is None:
            return

        user = await self.session.get(TelegramUser, queue.owner_id)
        if not user:
            return

        try:
            message = (
                f"📝 Новая заявка!\n\nПоступила новая заявка в очередь: {queue.name}"
                f"\nЦель визита: {event.purpose}\n\n"
                f"Дата: {event.preferred_date.strftime('%d.%m.%Y')} с "
                f"{event.preferred_time_start.strftime('%H:%M')} до {event.preferred_time_end.strftime('%H:%M')}"
            )
            await self.bot.send_message(user.telegram_id, message)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

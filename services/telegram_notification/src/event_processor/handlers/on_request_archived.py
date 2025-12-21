from logging import getLogger
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser
from .base import BaseEventHandler
from event_processor.events import RequestArchived


class OnRequestArchived(BaseEventHandler[RequestArchived]):
    @classmethod
    def event_type(cls) -> type[RequestArchived]:
        return RequestArchived

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_request_archived")

    async def __call__(self, event: RequestArchived) -> None:
        self.logger.info(
            f"Request {event.request_id} archived with status {event.status}"
        )

        result = await self.session.execute(
            select(TelegramUser).where(TelegramUser.user_id == event.user_id)
        )
        user = result.scalar_one_or_none()

        if not user or user.telegram_id == 0:
            return

        try:
            status_messages = {
                "completed": "✅ Заявка завершена",
                "rejected": "❌ Заявка отклонена и архивирована",
                "cancelled": "🚫 Заявка отменена и архивирована",
            }
            message = status_messages.get(
                event.status, f"📦 Заявка архивирована (статус: {event.status})"
            )
            message += f"\n\nID: {event.request_id}"

            await self.bot.send_message(user.telegram_id, message)
            self.logger.info(f"Notification sent to {user.telegram_id}")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser, Request, Queue
from .base import BaseEventHandler
from event_processor.events import CommentAdded


class OnCommentAdded(BaseEventHandler[CommentAdded]):
    @classmethod
    def event_type(cls) -> type[CommentAdded]:
        return CommentAdded

    def __init__(self, session: AsyncSession, bot: Bot):
        self.session = session
        self.bot = bot
        self.logger = getLogger("event_handler.on_comment_added")

    async def __call__(self, event: CommentAdded) -> None:
        self.logger.info(f"Comment added to request {event.request_id}")

        request = await self.session.get(Request, event.request_id)
        if not request:
            return

        queue = await self.session.get(Queue, request.queue_id)
        if not queue:
            return

        if event.author_id == queue.owner_id:
            notify_user_id = request.user_id
        else:
            notify_user_id = queue.owner_id

        user = await self.session.get(TelegramUser, notify_user_id)
        if not user or user.telegram_id == 0:
            return

        try:
            message = (
                f"💬 Новый комментарий к заявке\n\n"
                f"Очередь: {queue.name}\n"
                f"Комментарий: {event.comment_text}"
            )
            await self.bot.send_message(user.telegram_id, message)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

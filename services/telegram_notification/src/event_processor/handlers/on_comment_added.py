from logging import getLogger
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

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
        self.logger.info(
            f"💬 Комментарий к заявке {event.request_id}:\n"
            f"Автор: {event.author_id}\n"
            f"Текст: {event.comment_text}"
        )

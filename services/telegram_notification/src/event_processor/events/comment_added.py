from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class CommentAdded(BaseEvent):
    name: ClassVar[str] = "request.added_comment"

    request_id: UUID
    author_id: UUID
    comment_text: str

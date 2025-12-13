from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class AddedComment(DomainEvent):
    name: ClassVar[str] = "request.added_comment"

    request_id: UUID
    comment_text: str
    author_id: UUID

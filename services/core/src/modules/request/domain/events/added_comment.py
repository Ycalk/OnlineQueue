from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    Comment,
)
from modules.request.domain.aggregates import RequestId


class AddedComment(DomainEvent):
    request_id: RequestId
    comment: Comment

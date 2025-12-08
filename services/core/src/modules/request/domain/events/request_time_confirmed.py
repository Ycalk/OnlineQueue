from datetime import datetime
from uuid import UUID


from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestId,
    UserId,
    QueueId,
    RequestDateTime,
)


class RequestTimeConfirmed(DomainEvent):
    request_id: UUID
    user_id: UUID
    queue_id: UUID
    confirmed_datetime: RequestDateTime
    confirmed_at: datetime

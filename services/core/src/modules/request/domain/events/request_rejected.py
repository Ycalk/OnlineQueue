from datetime import datetime
from uuid import UUID


from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import RequestId, UserId, QueueId


class RequestRejected(DomainEvent):
    request_id: UUID
    user_id: UUID
    queue_id: UUID
    rejected_at: datetime
    reason: str | None = None

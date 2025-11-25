from datetime import datetime

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestId,
    UserId,
    QueueId,
    RequestDateTime,
)


class RequestTimeConfirmed(DomainEvent):
    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    confirmed_datetime: RequestDateTime
    confirmed_at: datetime

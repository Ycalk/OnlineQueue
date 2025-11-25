from datetime import datetime

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestId,
    UserId,
    QueueId,
    RequestDateTime,
)


class RequestAccepted(DomainEvent):
    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    accepted_at: datetime
    # Может быть принята без точного слота, либо с ним
    confirmed_datetime: RequestDateTime | None = None

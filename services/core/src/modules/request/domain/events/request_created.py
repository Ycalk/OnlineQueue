from datetime import datetime

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestId,
    UserId,
    QueueId,
    RequestPriority,
    RequestDateTime,
)


class RequestCreated(DomainEvent):
    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    priority: RequestPriority
    created_at: datetime
    # Заявка может быть создана без конкретной даты/интервала
    desired_datetime: RequestDateTime | None = None

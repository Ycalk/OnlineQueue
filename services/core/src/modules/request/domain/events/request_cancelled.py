from datetime import datetime

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import RequestId, UserId, QueueId


class RequestCancelled(DomainEvent):
    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    cancelled_at: datetime

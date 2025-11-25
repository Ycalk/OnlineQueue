from datetime import datetime

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import RequestId, UserId, QueueId


class RequestCompleted(DomainEvent):
    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    completed_at: datetime

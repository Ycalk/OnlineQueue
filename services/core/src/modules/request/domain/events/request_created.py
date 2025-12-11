from shared.building_blocks import DomainEvent
from modules.request.domain.aggregates import RequestId
from modules.request.domain.value_objects import (
    RequestPriority,
    RequestDatetime,
    RequestStatus,
    UserId,
    QueueId,
    Purpose,
)


class RequestCreated(DomainEvent):
    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    purpose: Purpose
    preferred_datetime: RequestDatetime
    priority: RequestPriority
    status: RequestStatus

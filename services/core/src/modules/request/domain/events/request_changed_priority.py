from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestPriority,
)
from modules.request.domain.aggregates import RequestId


class RequestChangedPriority(DomainEvent):
    request_id: RequestId
    new_priority: RequestPriority

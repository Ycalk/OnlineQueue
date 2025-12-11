from shared.building_blocks import DomainEvent
from modules.request.domain.aggregates import RequestId
from modules.request.domain.value_objects import (
    RequestDatetime,
)


class RequestChangedConfirmedDatetime(DomainEvent):
    request_id: RequestId
    new_confirmed_datetime: RequestDatetime

from datetime import datetime
from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import RequestId, UserId


class RequestArchived(DomainEvent):
    request_id: RequestId
    user_id: UserId
    request_created_at: datetime

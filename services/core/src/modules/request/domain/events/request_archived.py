from datetime import datetime

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import RequestId, UserId, QueueId


class RequestArchived(DomainEvent):
    """
    Событие архивирования заявки в bounded context `request`.
    """

    request_id: RequestId
    user_id: UserId
    queue_id: QueueId
    archived_at: datetime

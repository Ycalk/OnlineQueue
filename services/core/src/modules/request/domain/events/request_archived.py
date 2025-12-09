from datetime import datetime
from uuid import UUID

from shared.building_blocks import DomainEvent


class RequestArchived(DomainEvent):
    """
    Событие архивирования заявки в bounded context `request`.
    """

    request_id: UUID
    user_id: UUID
    queue_id: UUID
    archived_at: datetime

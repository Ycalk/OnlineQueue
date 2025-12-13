from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class CleanupPeriodChanged(DomainEvent):
    name: ClassVar[str] = "queue.cleanup_period_changed"

    queue_id: UUID
    old_cleanup_period_days: int
    new_cleanup_period_days: int

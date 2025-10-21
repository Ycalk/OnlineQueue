from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import (
    OwnerId,
    Name,
    Description,
    SlotDuration,
    CleanupPeriod,
)
from modules.queue.domain.aggregates import QueueId


class QueueCreated(DomainEvent):
    queue_id: QueueId
    owner_id: OwnerId
    name: Name
    description: Description
    slot_duration: SlotDuration
    cleanup_period: CleanupPeriod

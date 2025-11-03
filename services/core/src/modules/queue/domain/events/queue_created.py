from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import (
    Name,
    Description,
    TimePeriod,
    CleanupPeriod,
    UserId,
)
from modules.queue.domain.aggregates import QueueId


class QueueCreated(DomainEvent):
    queue_id: QueueId
    owner_id: UserId
    name: Name
    description: Description
    cleanup_period: CleanupPeriod
    reception_time: TimePeriod

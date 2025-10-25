from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import (
    Name,
    Description,
    TimePeriod,
    CleanupPeriod,
)
from modules.queue.domain.aggregates import QueueId
from modules.queue.domain.entities import User


class QueueCreated(DomainEvent):
    queue_id: QueueId
    owner: User
    name: Name
    description: Description
    cleanup_period: CleanupPeriod
    reception_time: TimePeriod

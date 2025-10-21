from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import CleanupPeriod
from modules.queue.domain.aggregates import QueueId


class CleanupPeriodChanged(DomainEvent):
    queue_id: QueueId
    old_cleanup_period: CleanupPeriod
    new_cleanup_period: CleanupPeriod

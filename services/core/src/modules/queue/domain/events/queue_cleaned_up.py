from shared.building_blocks import DomainEvent
from modules.queue.domain.aggregates import QueueId


class QueueCleanedUp(DomainEvent):
    queue_id: QueueId

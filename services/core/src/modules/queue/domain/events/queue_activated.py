from shared.building_blocks import DomainEvent
from modules.queue.domain.aggregates import QueueId


class QueueActivated(DomainEvent):
    queue_id: QueueId

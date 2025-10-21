from shared.building_blocks import DomainEvent
from modules.queue.domain.aggregates import QueueId


class QueueDeactivated(DomainEvent):
    queue_id: QueueId

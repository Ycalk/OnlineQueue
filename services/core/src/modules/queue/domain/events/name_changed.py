from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import Name
from modules.queue.domain.aggregates import QueueId


class NameChanged(DomainEvent):
    queue_id: QueueId
    old_name: Name
    new_name: Name

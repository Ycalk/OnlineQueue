from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import Description
from modules.queue.domain.aggregates import QueueId


class DescriptionChanged(DomainEvent):
    queue_id: QueueId
    old_description: Description
    new_description: Description

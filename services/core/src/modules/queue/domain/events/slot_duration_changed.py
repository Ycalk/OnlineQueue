from shared.building_blocks import DomainEvent
from modules.queue.domain.value_objects import SlotDuration
from modules.queue.domain.aggregates import QueueId


class MaxSlotDurationChanged(DomainEvent):
    queue_id: QueueId
    old_max_slot_duration: SlotDuration
    new_max_slot_duration: SlotDuration

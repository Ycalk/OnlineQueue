from dataclasses import dataclass
from typing import Self
from .id import QueueId
from modules.queue.domain.value_objects import (
    OwnerId,
    Name,
    Description,
    SlotDuration,
    CleanupPeriod,
)
from modules.queue.domain.events import QueueCreated
from shared.building_blocks import AggregateRoot


@dataclass
class Queue(AggregateRoot):
    id: QueueId
    owner_id: OwnerId
    name: Name
    description: Description
    slot_duration: SlotDuration
    cleanup_period: CleanupPeriod

    @classmethod
    def create(
        cls,
        owner_id: OwnerId,
        name: Name,
        description: Description,
        slot_duration: SlotDuration,
        cleanup_period: CleanupPeriod,
    ) -> Self:
        queue = cls(
            id=QueueId(),
            owner_id=owner_id,
            name=name,
            description=description,
            slot_duration=slot_duration,
            cleanup_period=cleanup_period,
        )
        queue._add_event(
            QueueCreated(
                queue_id=queue.id,
                owner_id=owner_id,
                name=name,
                description=description,
                slot_duration=slot_duration,
                cleanup_period=cleanup_period,
            )
        )
        return queue

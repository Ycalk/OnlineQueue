from dataclasses import dataclass, field
from typing import Self
from .id import QueueId
from modules.queue.domain.value_objects import (
    Name,
    IsActive,
    Description,
    SlotDuration,
    CleanupPeriod,
)
from modules.queue.domain.entities import User, Request
from modules.queue.domain.events import (
    QueueCreated,
    NameChanged,
    DescriptionChanged,
    MaxSlotDurationChanged,
    CleanupPeriodChanged,
    QueueActivated,
    QueueDeactivated,
)
from shared.building_blocks import AggregateRoot
from modules.queue.domain.errors import (
    CannotChangeSlotDuration,
    CannotActivateAlreadyActiveQueue,
    CannotDeactivateAlreadyDeactivatedQueue,
)


@dataclass
class Queue(AggregateRoot):
    id: QueueId
    owner: User
    name: Name
    description: Description
    max_slot_duration: SlotDuration
    cleanup_period: CleanupPeriod
    is_active: IsActive = field(default=IsActive(value=True))
    requests: list[Request] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        owner: User,
        name: Name,
        description: Description,
        max_slot_duration: SlotDuration,
        cleanup_period: CleanupPeriod,
    ) -> Self:
        queue = cls(
            id=QueueId(),
            owner=owner,
            name=name,
            description=description,
            max_slot_duration=max_slot_duration,
            cleanup_period=cleanup_period,
        )
        queue._add_event(
            QueueCreated(
                queue_id=queue.id,
                owner=owner,
                name=name,
                description=description,
                max_slot_duration=max_slot_duration,
                cleanup_period=cleanup_period,
            )
        )
        return queue

    def change_name(self, new_name: Name) -> None:
        event = NameChanged(
            queue_id=self.id,
            old_name=self.name,
            new_name=new_name,
        )
        self.name = new_name
        self._add_event(event)

    def change_description(self, new_description: Description) -> None:
        event = DescriptionChanged(
            queue_id=self.id,
            old_description=self.description,
            new_description=new_description,
        )
        self.description = new_description
        self._add_event(event)

    def change_max_slot_duration(self, new_max_slot_duration: SlotDuration) -> None:
        if any(
            request.slot_duration.value_minutes > new_max_slot_duration.value_minutes
            for request in self.requests
        ):
            raise CannotChangeSlotDuration(
                (
                    f"Cannot change max slot duration to {new_max_slot_duration.value_minutes} minutes"
                    " because there are requests with slot duration"
                    f" greater than {new_max_slot_duration.value_minutes} minutes"
                )
            )
        event = MaxSlotDurationChanged(
            queue_id=self.id,
            old_max_slot_duration=self.max_slot_duration,
            new_max_slot_duration=new_max_slot_duration,
        )
        self.max_slot_duration = new_max_slot_duration
        self._add_event(event)

    def change_cleanup_period(self, new_cleanup_period: CleanupPeriod) -> None:
        event = CleanupPeriodChanged(
            queue_id=self.id,
            old_cleanup_period=self.cleanup_period,
            new_cleanup_period=new_cleanup_period,
        )
        self.cleanup_period = new_cleanup_period
        self._add_event(event)

    def deactivate(self) -> None:
        if not self.is_active.value:
            raise CannotDeactivateAlreadyDeactivatedQueue(
                f"Queue {self.id.value} is already deactivated"
            )
        self.is_active = IsActive(value=False)
        self._add_event(QueueDeactivated(queue_id=self.id))

    def activate(self) -> None:
        if self.is_active.value:
            raise CannotActivateAlreadyActiveQueue(
                f"Queue {self.id.value} is already active"
            )
        self.is_active = IsActive(value=True)
        self._add_event(QueueActivated(queue_id=self.id))

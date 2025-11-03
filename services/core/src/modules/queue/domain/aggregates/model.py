from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
from .id import QueueId
from modules.queue.domain.value_objects import (
    Name,
    IsActive,
    Description,
    CleanupPeriod,
    TimePeriod,
    RequestStatus,
    UserId,
)
from modules.queue.domain.entities import Request
from modules.queue.domain.events import (
    QueueCreated,
    NameChanged,
    DescriptionChanged,
    CleanupPeriodChanged,
    QueueActivated,
    QueueDeactivated,
    RequestArchived,
    QueueCleanedUp,
)
from shared.building_blocks import AggregateRoot
from modules.queue.domain.errors import (
    CannotActivateActiveQueue,
    CannotDeactivateAlreadyDeactivatedQueue,
)


@dataclass
class Queue(AggregateRoot):
    id: QueueId
    owner_id: UserId
    name: Name
    description: Description
    cleanup_period: CleanupPeriod
    reception_time: TimePeriod
    is_active: IsActive = field(default=IsActive(value=True))
    requests: list[Request] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        owner_id: UserId,
        name: Name,
        description: Description,
        cleanup_period: CleanupPeriod,
        reception_time: TimePeriod,
    ) -> Self:
        queue = cls(
            id=QueueId(),
            owner_id=owner_id,
            name=name,
            description=description,
            cleanup_period=cleanup_period,
            reception_time=reception_time,
        )
        queue._add_event(
            QueueCreated(
                queue_id=queue.id,
                owner_id=owner_id,
                name=name,
                description=description,
                cleanup_period=cleanup_period,
                reception_time=reception_time,
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

    def change_cleanup_period(self, new_cleanup_period: CleanupPeriod) -> None:
        event = CleanupPeriodChanged(
            queue_id=self.id,
            old_cleanup_period=self.cleanup_period,
            new_cleanup_period=new_cleanup_period,
        )
        self.cleanup_period = new_cleanup_period
        self._add_event(event)

    def cleanup(self) -> None:
        current_time = datetime.now().timestamp()
        for request in (request for request in self.requests if not request.archived):
            if (
                request.status == RequestStatus.PENDING
                and request.created_at.timestamp()
                < current_time - self.cleanup_period.value_seconds
            ):
                request.archive()
                self._add_event(
                    RequestArchived(
                        request_id=request.id,
                        user_id=request.user_id,
                        request_created_at=request.created_at,
                    )
                )
            elif request.status == RequestStatus.REJECTED:
                request.archive()
                self._add_event(
                    RequestArchived(
                        request_id=request.id,
                        user_id=request.user_id,
                        request_created_at=request.created_at,
                    )
                )
            elif (
                request.status == RequestStatus.ACCEPTED
                and request.confirmed_time is not None
                and request.confirmed_time.end_period.timestamp()
                < current_time - self.cleanup_period.value_seconds
            ):
                request.archive()
                self._add_event(
                    RequestArchived(
                        request_id=request.id,
                        user_id=request.user_id,
                        request_created_at=request.created_at,
                    )
                )

        self._add_event(QueueCleanedUp(queue_id=self.id))

    def deactivate(self) -> None:
        if not self.is_active.value:
            raise CannotDeactivateAlreadyDeactivatedQueue(
                f"Queue {self.id.value} is already deactivated"
            )
        self.is_active = IsActive(value=False)
        self._add_event(QueueDeactivated(queue_id=self.id))

    def activate(self) -> None:
        if self.is_active.value:
            raise CannotActivateActiveQueue(f"Queue {self.id.value} is already active")
        self.is_active = IsActive(value=True)
        self._add_event(QueueActivated(queue_id=self.id))

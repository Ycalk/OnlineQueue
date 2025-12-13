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
    RequestId,
    RequestDateTime,
    RequestPriority,
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
    RequestRequeued,
    RequestRejected,
)
from shared.building_blocks import AggregateRoot
from modules.queue.domain.errors import (
    CannotActivateActiveQueue,
    CannotDeactivateAlreadyDeactivatedQueue,
    RequestIsNotPending,
    TimeMustBeInsideQueueReceptionTime,
    RequestNotFound,
    RequestIsFrozen,
    CannotScheduleRequest,
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
                queue_id=queue.id.value,
                owner_id=owner_id.value,
                queue_name=name.value,
                description=description.value,
                cleanup_period_days=cleanup_period.value_days,
                reception_time_start=reception_time.start_time,
                reception_time_end=reception_time.end_time,
            )
        )
        return queue

    def change_name(self, new_name: Name) -> None:
        event = NameChanged(
            queue_id=self.id.value,
            old_name=self.name.value,
            new_name=new_name.value,
        )
        self.name = new_name
        self._add_event(event)

    def change_description(self, new_description: Description) -> None:
        event = DescriptionChanged(
            queue_id=self.id.value,
            old_description=self.description.value,
            new_description=new_description.value,
        )
        self.description = new_description
        self._add_event(event)

    def change_cleanup_period(self, new_cleanup_period: CleanupPeriod) -> None:
        event = CleanupPeriodChanged(
            queue_id=self.id.value,
            old_cleanup_period_days=self.cleanup_period.value_days,
            new_cleanup_period_days=new_cleanup_period.value_days,
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
                        request_id=request.id.value,
                        user_id=request.user_id.value,
                        request_created_at=request.created_at,
                    )
                )
            elif request.status == RequestStatus.REJECTED:
                request.archive()
                self._add_event(
                    RequestArchived(
                        request_id=request.id.value,
                        user_id=request.user_id.value,
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
                        request_id=request.id.value,
                        user_id=request.user_id.value,
                        request_created_at=request.created_at,
                    )
                )

        self._add_event(QueueCleanedUp(queue_id=self.id.value))

    def deactivate(self) -> None:
        if not self.is_active.value:
            raise CannotDeactivateAlreadyDeactivatedQueue(
                f"Queue {self.id.value} is already deactivated"
            )
        self.is_active = IsActive(value=False)
        for request in self.requests:
            if request.status == RequestStatus.REJECTED or request.archived:
                continue
            request.reject()
            self._add_event(RequestRejected(request_id=request.id.value))
        self._add_event(QueueDeactivated(queue_id=self.id.value))

    def activate(self) -> None:
        if self.is_active.value:
            raise CannotActivateActiveQueue(f"Queue {self.id.value} is already active")
        self.is_active = IsActive(value=True)
        self._add_event(QueueActivated(queue_id=self.id.value))

    def calculate_average_requests_duration_seconds(self) -> int | None:
        sum_duration = 0
        count = 0
        for request in self.requests:
            if request.archived:
                continue
            if (duration := request.calculate_duration_seconds()) is not None:
                sum_duration += duration
                count += 1
        if count == 0:
            return None
        return round(sum_duration / count)

    # Event handlers
    def on_request_created(self, request: Request) -> None:
        if request.status != RequestStatus.PENDING:
            raise RequestIsNotPending(
                f"Can only add requests with status PENDING, got {request.status}"
            )
        if not request.preferred_time.time_period.is_inside(self.reception_time):
            raise TimeMustBeInsideQueueReceptionTime(
                "Preferred visiting time must be inside queue reception time"
            )
        self.requests.append(request)

    def _can_displace(self, candidate: Request, incumbent: Request) -> bool:
        """
        Определяет, может ли кандидат (новая/изменяемая заявка) вытеснить существующую (incumbent).
        Правила:
        - Если приоритет кандидата выше -> True.
        - Если приоритет одинаковый -> смотрим на created_at (кто старее, тот и прав).
           Если кандидат создан раньше (более старый), то он вытесняет -> True.
        - Иначе -> False.
        """
        priority_map = {
            RequestPriority.HIGH: 3,
            RequestPriority.MEDIUM: 2,
            RequestPriority.LOW: 1,
        }
        return priority_map[candidate.priority] > priority_map[incumbent.priority] or (
            priority_map[candidate.priority] == priority_map[incumbent.priority]
            and candidate.created_at < incumbent.created_at
        )

    def on_change_request_confirmed_time(
        self, request_id: RequestId, confirmed_time: RequestDateTime
    ) -> None:
        target_request = next(
            (
                request
                for request in self.requests
                if request.id.value == request_id.value
            ),
            None,
        )
        if target_request is None:
            raise RequestNotFound(f"Request {request_id.value} not found")

        if target_request.status == RequestStatus.REJECTED or target_request.archived:
            raise RequestIsFrozen(
                f"Request {request_id.value} is frozen and cannot be updated"
            )

        conflicts: list[Request] = []

        for req in self.requests:
            if (
                req.id.value == target_request.id.value
                or req.status != RequestStatus.ACCEPTED
                or req.confirmed_time is None
                or req.archived
            ):
                continue
            if req.confirmed_time.check_intersection(confirmed_time):
                conflicts.append(req)

        if len(conflicts) == 0:
            target_request.confirmed_time = confirmed_time
            target_request.status = RequestStatus.ACCEPTED
            return

        if all(self._can_displace(target_request, conflict) for conflict in conflicts):
            for conflict in conflicts:
                conflict.confirmed_time = None
                conflict.status = RequestStatus.PENDING
                self._add_event(
                    RequestRequeued(
                        request_id=conflict.id.value,
                    )
                )
            target_request.confirmed_time = confirmed_time
            target_request.status = RequestStatus.ACCEPTED
        else:
            raise CannotScheduleRequest(
                f"Request {request_id.value} cannot be scheduled due to conflicts."
            )

    def on_change_request_priority(
        self, request_id: RequestId, new_priority: RequestPriority
    ):
        target_request = next(
            (
                request
                for request in self.requests
                if request.id.value == request_id.value
            ),
            None,
        )
        if target_request is None:
            raise RequestNotFound(f"Request {request_id.value} not found")

        if target_request.status == RequestStatus.REJECTED or target_request.archived:
            raise RequestIsFrozen(
                f"Request {request_id.value} is frozen and cannot be updated"
            )

        target_request.priority = new_priority

    def on_request_rejected(self, request_id: RequestId):
        target_request = next(
            (
                request
                for request in self.requests
                if request.id.value == request_id.value
            ),
            None,
        )
        if target_request is None:
            raise RequestNotFound(f"Request {request_id.value} not found")

        if target_request.status == RequestStatus.REJECTED or target_request.archived:
            raise RequestIsFrozen(
                f"Request {request_id.value} is frozen and cannot be updated"
            )

        target_request.status = RequestStatus.REJECTED
        target_request.archived = True

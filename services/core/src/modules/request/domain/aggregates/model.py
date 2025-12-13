from dataclasses import dataclass, field

from shared.building_blocks import AggregateRoot
from .id import RequestId
from modules.request.domain.entities import Queue
from modules.request.domain.value_objects import (
    Purpose,
    UserId,
    RequestStatus,
    RequestPriority,
    RequestDatetime,
    RequestStatusHistoryItem,
    RequestConfirmationDatetimeHistoryItem,
    RequestPriorityHistoryItem,
    Comment,
    CommentAuthor,
)
from modules.request.domain.events import (
    RequestCreated,
    RequestAccepted,
    RequestRejected,
    RequestChangedConfirmedDatetime,
    RequestChangedPriority,
    AddedComment,
)
from modules.request.domain.errors import (
    RejectedRequestIsFrozen,
    ArchivedRequestIsFrozen,
    PreferredVisitingTimeMustBeInsideQueueReceptionTime,
    CannotCreateRequestToInactiveQueue,
)


@dataclass
class Request(AggregateRoot):
    # Идентификаторы и базовые данные
    id: RequestId
    purpose: Purpose
    user_id: UserId
    queue: Queue

    preferred_datetime: RequestDatetime

    # История статусов и подтверждений
    status_history: list[RequestStatusHistoryItem] = field(default_factory=list)
    confirmation_datetime_history: list[RequestConfirmationDatetimeHistoryItem] = field(
        default_factory=list
    )
    priority_history: list[RequestPriorityHistoryItem] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)

    # Архивация
    archived: bool = field(default=False)

    @property
    def status(self) -> RequestStatus:
        return max(self.status_history, key=lambda x: x.occurred_at).status

    @property
    def priority(self) -> RequestPriority:
        return max(self.priority_history, key=lambda x: x.occurred_at).priority

    @property
    def confirmed_datetime(self) -> RequestDatetime | None:
        return (
            max(
                self.confirmation_datetime_history,
                key=lambda x: x.confirmation_datetime.time_period.start_time,
            ).confirmation_datetime
            if len(self.confirmation_datetime_history) > 0
            else None
        )

    @classmethod
    def create(
        cls,
        user_id: UserId,
        queue: Queue,
        purpose: Purpose,
        preferred_datetime: RequestDatetime,
        priority: RequestPriority = RequestPriority.MEDIUM,
    ) -> "Request":
        if not queue.is_active:
            raise CannotCreateRequestToInactiveQueue(
                f"Queue {queue.id.value} is inactive"
            )

        if not preferred_datetime.time_period.is_inside(queue.reception_time):
            raise PreferredVisitingTimeMustBeInsideQueueReceptionTime(
                "Preferred visiting time must be inside queue reception time"
            )

        request = cls(
            id=RequestId(),
            purpose=purpose,
            user_id=user_id,
            queue=queue,
            preferred_datetime=preferred_datetime,
        )

        request.status_history.append(
            RequestStatusHistoryItem(status=RequestStatus.PENDING)
        )

        request.priority_history.append(RequestPriorityHistoryItem(priority=priority))

        request._add_event(
            RequestCreated(
                request_id=request.id.value,
                user_id=user_id.value,
                queue_id=queue.id.value,
                purpose=purpose.value,
                preferred_date=preferred_datetime.date,
                preferred_time_start=preferred_datetime.time_period.start_time,
                preferred_time_end=preferred_datetime.time_period.end_time,
                priority=priority,
                status=RequestStatus.PENDING,
            )
        )

        return request

    # ---------- Команды домена ----------

    def update_confirmation_datetime(
        self, new_confirmed_datetime: RequestDatetime
    ) -> None:
        if self.status == RequestStatus.REJECTED:
            raise RejectedRequestIsFrozen(
                "Rejected request confirmation datetime is unchangeable"
            )

        if self.archived:
            raise ArchivedRequestIsFrozen(
                "Archived request confirmation datetime is unchangeable"
            )

        self.confirmation_datetime_history.append(
            RequestConfirmationDatetimeHistoryItem(
                confirmation_datetime=new_confirmed_datetime
            )
        )
        if self.status == RequestStatus.PENDING:
            self.status_history.append(
                RequestStatusHistoryItem(status=RequestStatus.ACCEPTED)
            )
            self._add_event(
                RequestAccepted(
                    request_id=self.id.value,
                    confirmed_date=new_confirmed_datetime.date,
                    confirmed_time_start=new_confirmed_datetime.time_period.start_time,
                    confirmed_time_end=new_confirmed_datetime.time_period.end_time,
                )
            )
        else:
            self._add_event(
                RequestChangedConfirmedDatetime(
                    request_id=self.id.value,
                    new_confirmed_date=new_confirmed_datetime.date,
                    new_confirmed_time_start=new_confirmed_datetime.time_period.start_time,
                    new_confirmed_time_end=new_confirmed_datetime.time_period.end_time,
                )
            )

    def update_priority(self, new_priority: RequestPriority) -> None:
        if self.status == RequestStatus.REJECTED:
            raise RejectedRequestIsFrozen("Rejected request priority is unchangeable")

        if self.archived:
            raise ArchivedRequestIsFrozen("Archived request priority is unchangeable")

        self.priority_history.append(RequestPriorityHistoryItem(priority=new_priority))
        self._add_event(
            RequestChangedPriority(request_id=self.id.value, new_priority=new_priority)
        )

    def reject(self) -> None:
        if self.status == RequestStatus.REJECTED:
            raise RejectedRequestIsFrozen("Rejected request priority is unchangeable")

        if self.archived:
            raise ArchivedRequestIsFrozen("Archived request priority is unchangeable")

        self.status_history.append(
            RequestStatusHistoryItem(status=RequestStatus.REJECTED)
        )

        self._add_event(RequestRejected(request_id=self.id.value))

    def add_comment(self, comment: Comment) -> None:
        if self.status == RequestStatus.REJECTED:
            raise RejectedRequestIsFrozen("Rejected request priority is unchangeable")

        if self.archived:
            raise ArchivedRequestIsFrozen("Archived request priority is unchangeable")

        self.comments.append(comment)
        self._add_event(
            AddedComment(
                request_id=self.id.value,
                comment_text=comment.text,
                author_id=self.user_id.value
                if comment.author == CommentAuthor.VISITER
                else self.queue.owner_id.value,
            )
        )

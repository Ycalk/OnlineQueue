from dataclasses import dataclass, field
from datetime import datetime

from shared.building_blocks import AggregateRoot
from modules.request.domain.value_objects import (
    RequestId,
    UserId,
    QueueId,
    RequestStatus,
    RequestPriority,
    RequestDateTime,
    RequestStatusHistoryItem,
    RequestConfirmationHistoryItem,
)
from modules.request.domain.events import (
    RequestCreated,
    RequestCancelled,
    RequestAccepted,
    RequestRejected,
    RequestCompleted,
    RequestTimeConfirmed,
    RequestArchived,    
)


@dataclass
class Request(AggregateRoot):
    # Идентификаторы и базовые данные
    id: RequestId
    purpose: str
    user_id: UserId
    queue_id: QueueId

    # Статус и приоритет
    status: RequestStatus
    priority: RequestPriority

    # Время создания/обновления
    created_at: datetime
    updated_at: datetime | None = None

    # Предпочитаемое и подтверждённое время записи
    preferred_datetime: RequestDateTime | None = None
    confirmed_datetime: RequestDateTime | None = None

    # История статусов и подтверждений
    status_history: list[RequestStatusHistoryItem] = field(default_factory=list)
    confirmation_history: list[RequestConfirmationHistoryItem] = field(default_factory=list)

    # Архивация
    archived: bool = field(default=False)

    # ---------- Фабрика ----------

    @classmethod
    def create(
        cls,
        user_id: UserId,
        queue_id: QueueId,
        purpose: str,
        priority: RequestPriority = RequestPriority.MEDIUM,
        preferred_datetime: RequestDateTime | None = None,
    ) -> "Request":
        now = datetime.utcnow()

        request = cls(
            id=RequestId(),
            purpose=purpose,
            user_id=user_id,
            queue_id=queue_id,
            status=RequestStatus.PENDING,
            priority=priority,
            created_at=now,
            updated_at=now,
            preferred_datetime=preferred_datetime,
        )

        request.status_history.append(
            RequestStatusHistoryItem(status=RequestStatus.PENDING, updated_at=now)
        )

        if preferred_datetime is not None:
            request.confirmation_history.append(
                RequestConfirmationHistoryItem(
                    date=preferred_datetime.date,
                    time_start=preferred_datetime.time_period.start_time,
                    time_end=preferred_datetime.time_period.end_time,
                    updated_at=now,
                )
            )

        request._add_event(
            RequestCreated(
                request_id=request.id,
                user_id=user_id,
                queue_id=queue_id,
                priority=priority,
                created_at=now,
                desired_datetime=preferred_datetime,
            )
        )

        return request

    # ---------- Команды домена ----------

    def cancel(self) -> None:
        if self.archived:
            return

        if self.status in (
            RequestStatus.REJECTED,
            RequestStatus.COMPLETED,
            RequestStatus.CANCELLED,
        ):
            return

        now = datetime.utcnow()
        self.status = RequestStatus.CANCELLED
        self.updated_at = now

        self.status_history.append(
            RequestStatusHistoryItem(status=self.status, updated_at=now)
        )

        self._add_event(
            RequestCancelled(
                request_id=self.id,
                user_id=self.user_id,
                queue_id=self.queue_id,
                cancelled_at=now,
            )
        )

    def accept(self, confirmed_datetime: RequestDateTime | None = None) -> None:
        if self.archived:
            return

        if self.status is not RequestStatus.PENDING:
            return

        now = datetime.utcnow()
        self.status = RequestStatus.ACCEPTED
        self.updated_at = now

        self.status_history.append(
            RequestStatusHistoryItem(status=self.status, updated_at=now)
        )

        if confirmed_datetime is not None:
            self.confirmed_datetime = confirmed_datetime
            self.confirmation_history.append(
                RequestConfirmationHistoryItem(
                    date=confirmed_datetime.date,
                    time_start=confirmed_datetime.time_period.start_time,
                    time_end=confirmed_datetime.time_period.end_time,
                    updated_at=now,
                )
            )
            self._add_event(
                RequestTimeConfirmed(
                    request_id=self.id,
                    user_id=self.user_id,
                    queue_id=self.queue_id,
                    confirmed_datetime=confirmed_datetime,
                    confirmed_at=now,
                )
            )

        self._add_event(
            RequestAccepted(
                request_id=self.id,
                user_id=self.user_id,
                queue_id=self.queue_id,
                accepted_at=now,
                confirmed_datetime=self.confirmed_datetime,
            )
        )

    def reject(self, reason: str | None = None) -> None:
        if self.archived:
            return

        if self.status is not RequestStatus.PENDING:
            return

        now = datetime.utcnow()
        self.status = RequestStatus.REJECTED
        self.updated_at = now

        self.status_history.append(
            RequestStatusHistoryItem(status=self.status, updated_at=now)
        )

        self._add_event(
            RequestRejected(
                request_id=self.id,
                user_id=self.user_id,
                queue_id=self.queue_id,
                rejected_at=now,
                reason=reason,
            )
        )

    def complete(self) -> None:
        if self.archived:
            return

        if self.status is not RequestStatus.ACCEPTED:
            return

        now = datetime.utcnow()
        self.status = RequestStatus.COMPLETED
        self.updated_at = now

        self.status_history.append(
            RequestStatusHistoryItem(status=self.status, updated_at=now)
        )

        self._add_event(
            RequestCompleted(
                request_id=self.id,
                user_id=self.user_id,
                queue_id=self.queue_id,
                completed_at=now,
            )
        )

    def archive(self) -> None:
        if self.archived:
            return

        now = datetime.utcnow()
        self.archived = True
        self.updated_at = now

        self._add_event(
            RequestArchived(
                request_id=self.id,
                user_id=self.user_id,
                queue_id=self.queue_id,
                archived_at=now,
            )
        )

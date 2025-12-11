from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.domain.aggregates import Request as RequestAggregate
from modules.request.domain.aggregates import RequestId
from modules.request.domain.entities import Queue
from modules.request.domain.value_objects import (
    QueueId,
    UserId,
    RequestDatetime,
    TimePeriod,
    RequestStatus,
    RequestPriority,
    CommentAuthor,
    RequestStatusHistoryItem as StatusHistoryVO,
    RequestConfirmationDatetimeHistoryItem as ConfirmationHistoryVO,
    RequestPriorityHistoryItem as PriorityHistoryVO,
    Comment as CommentVO,
    Purpose,
    IsActive,
)
from .models import (
    Request as RequestSchema,
    Queue as QueueSchema,
)


class RequestReader(IRequestReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, request_id: UUID) -> RequestAggregate | None:
        stmt = (
            select(RequestSchema)
            .options(
                selectinload(RequestSchema.queue),
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_datetime_history),
                selectinload(RequestSchema.priority_history),
                selectinload(RequestSchema.comments),
            )
            .where(RequestSchema.id == request_id)
        )
        result = await self._session.execute(stmt)
        request_model = result.scalar_one_or_none()

        if not request_model:
            return None

        return self._to_domain(request_model)

    async def find_queue_by_id(self, queue_id: UUID) -> Queue | None:
        stmt = select(QueueSchema).where(QueueSchema.id == queue_id)
        result = await self._session.execute(stmt)
        queue_model = result.scalar_one_or_none()

        if not queue_model:
            return None

        return self._queue_to_domain(queue_model)

    async def get_by_user_id(
        self, user_id: UUID, skip: int, limit: int | None
    ) -> list[RequestAggregate]:
        stmt = (
            select(RequestSchema)
            .options(
                selectinload(RequestSchema.queue),
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_datetime_history),
                selectinload(RequestSchema.priority_history),
                selectinload(RequestSchema.comments),
            )
            .where(RequestSchema.user_id == user_id)
            .offset(skip)
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def get_by_queue_owner_id(self, owner_id: UUID) -> list[RequestAggregate]:
        stmt = (
            select(RequestSchema)
            .join(QueueSchema, RequestSchema.queue_id == QueueSchema.id)
            .options(
                selectinload(RequestSchema.queue),
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_datetime_history),
                selectinload(RequestSchema.priority_history),
                selectinload(RequestSchema.comments),
            )
            .where(QueueSchema.owner_id == owner_id)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def get_by_queue_id(self, queue_id: UUID) -> list[RequestAggregate]:
        stmt = (
            select(RequestSchema)
            .options(
                selectinload(RequestSchema.queue),
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_datetime_history),
                selectinload(RequestSchema.priority_history),
                selectinload(RequestSchema.comments),
            )
            .where(RequestSchema.queue_id == queue_id)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: RequestSchema) -> RequestAggregate:
        request_id = RequestId(value=model.id)
        user_id = UserId(value=model.user_id)
        purpose = Purpose(value=model.purpose)

        preferred_datetime = RequestDatetime(
            date=model.preferred_date,
            time_period=TimePeriod(
                start_time=model.preferred_time_start, end_time=model.preferred_time_end
            ),
        )

        status_history = [
            StatusHistoryVO(
                status=RequestStatus(item.status), occurred_at=item.occurred_at
            )
            for item in model.status_history
        ]

        priority_history = [
            PriorityHistoryVO(
                priority=RequestPriority(item.priority), occurred_at=item.occurred_at
            )
            for item in model.priority_history
        ]

        confirmation_history = [
            ConfirmationHistoryVO(
                confirmation_datetime=RequestDatetime(
                    date=item.date,
                    time_period=TimePeriod(
                        start_time=item.time_start, end_time=item.time_end
                    ),
                ),
                occurred_at=item.occurred_at,
            )
            for item in model.confirmation_datetime_history
        ]

        comments = [
            CommentVO(
                author=CommentAuthor(item.author),
                text=item.text,
                created_at=item.created_at,
            )
            for item in model.comments
        ]

        return RequestAggregate(
            id=request_id,
            purpose=purpose,
            user_id=user_id,
            queue=self._queue_to_domain(model.queue),
            preferred_datetime=preferred_datetime,
            status_history=status_history,
            confirmation_datetime_history=confirmation_history,
            priority_history=priority_history,
            comments=comments,
            archived=model.archived,
        )

    def _queue_to_domain(self, model: QueueSchema) -> Queue:
        return Queue(
            id=QueueId(value=model.id),
            owner_id=UserId(value=model.owner_id),
            is_active=IsActive(value=model.is_active),
            reception_time=TimePeriod(
                start_time=model.reception_time_start,
                end_time=model.reception_time_end,
            ),
        )

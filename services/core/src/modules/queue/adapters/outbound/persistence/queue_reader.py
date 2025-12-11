from uuid import UUID

from modules.queue.application.ports.outbound.queue_reader import IQueueReader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .models import Queue as QueueSchema
from .models import Request as RequestSchema
from modules.queue.domain.aggregates import Queue, QueueId
from modules.queue.domain.value_objects import (
    Name,
    Description,
    IsActive,
    CleanupPeriod,
    TimePeriod,
    UserId,
    RequestId,
    RequestDateTime,
    RequestStatus,
)
from modules.queue.domain.entities import Request


class QueueReader(IQueueReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, queue_id: UUID) -> Queue | None:
        result = await self._session.execute(
            select(QueueSchema)
            .where(QueueSchema.id == queue_id)
            .options(selectinload(QueueSchema.requests))
        )
        queue_model = result.scalar_one_or_none()

        if queue_model is None:
            return None

        return self._queue_to_domain(queue_model)

    async def get_many(self, skip: int, limit: int | None) -> list[Queue]:
        result = await self._session.execute(
            select(QueueSchema)
            .offset(skip)
            .limit(limit)
            .options(selectinload(QueueSchema.requests))
        )

        return [
            self._queue_to_domain(queue_model) for queue_model in result.scalars().all()
        ]

    async def find_by_owner_id(self, owner_id: UUID) -> list[Queue]:
        result = await self._session.execute(
            select(QueueSchema)
            .where(QueueSchema.owner_id == owner_id)
            .options(selectinload(QueueSchema.requests))
        )
        return [
            self._queue_to_domain(queue_model) for queue_model in result.scalars().all()
        ]

    def _queue_to_domain(self, model: QueueSchema) -> Queue:
        return Queue(
            id=QueueId(value=model.id),
            owner_id=UserId(value=model.owner_id),
            name=Name(value=model.name),
            description=Description(value=model.description),
            cleanup_period=CleanupPeriod(value_days=model.clean_up_period_days),
            reception_time=TimePeriod(
                start_time=model.reception_time_start,
                end_time=model.reception_time_end,
            ),
            is_active=IsActive(value=model.is_active),
            requests=[self._request_to_domain(request) for request in model.requests],
        )

    def _request_to_domain(self, model: RequestSchema) -> Request:
        return Request(
            id=RequestId(value=model.id),
            user_id=UserId(value=model.user_id),
            preferred_time=RequestDateTime(
                date=model.preferred_date,
                time_period=TimePeriod(
                    start_time=model.preferred_time_start,
                    end_time=model.preferred_time_end,
                ),
            ),
            confirmed_time=RequestDateTime(
                date=model.confirmed_date,
                time_period=TimePeriod(
                    start_time=model.confirmed_time_start,
                    end_time=model.confirmed_time_end,
                ),
            )
            if model.confirmed_date
            and model.confirmed_time_start
            and model.confirmed_time_end
            else None,
            archived=model.archived,
            created_at=model.created_at,
            status=RequestStatus(value=model.status),
        )

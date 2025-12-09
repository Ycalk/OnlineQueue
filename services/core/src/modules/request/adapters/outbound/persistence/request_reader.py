from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.domain.aggregates import Request as RequestAggregate
from modules.request.domain.value_objects import (
    RequestId,
    QueueId,
    UserId,
    RequestDateTime,
    TimePeriod,
    RequestStatus,
    RequestPriority,
    RequestStatusHistoryItem as StatusHistoryVO,
    RequestConfirmationHistoryItem as ConfirmationHistoryVO,
)
from .models import RequestModel as RequestSchema


class RequestReader(IRequestReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, request_id: UUID) -> RequestAggregate | None:
        result = await self._session.execute(
            select(RequestSchema)
            .where(RequestSchema.id == request_id)
            .options(
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_history),
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._request_to_domain(model)

    async def get_many(self, skip: int, limit: int | None) -> list[RequestAggregate]:
        result = await self._session.execute(
            select(RequestSchema)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_history),
            )
        )
        return [self._request_to_domain(m) for m in result.scalars().all()]

    async def find_by_user_id(self, user_id: UUID) -> list[RequestAggregate]:
        result = await self._session.execute(
            select(RequestSchema)
            .where(RequestSchema.user_id == user_id)
            .options(
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_history),
            )
        )
        return [self._request_to_domain(m) for m in result.scalars().all()]

    async def find_by_queue_id(self, queue_id: UUID) -> list[RequestAggregate]:
        result = await self._session.execute(
            select(RequestSchema)
            .where(RequestSchema.queue_id == queue_id)
            .options(
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_history),
            )
        )
        return [self._request_to_domain(m) for m in result.scalars().all()]

    # --- маппинг в домен ---

    def _request_to_domain(self, model: RequestSchema) -> RequestAggregate:
        preferred_datetime = (
            RequestDateTime(
                date=model.preferred_date,
                time_period=TimePeriod(
                    start_time=model.preferred_time_start,
                    end_time=model.preferred_time_end,
                ),
            )
            if model.preferred_date and model.preferred_time_start and model.preferred_time_end
            else None
        )

        confirmed_datetime = (
            RequestDateTime(
                date=model.confirmed_date,
                time_period=TimePeriod(
                    start_time=model.confirmed_time_start,
                    end_time=model.confirmed_time_end,
                ),
            )
            if model.confirmed_date
            and model.confirmed_time_start
            and model.confirmed_time_end
            else None
        )

        status_history = [
            StatusHistoryVO(
                status=RequestStatus(value=history.status),
                updated_at=history.updated_at,
            )
            for history in model.status_history
        ]

        confirmation_history = [
            ConfirmationHistoryVO(
                date=history.date,
                time_start=history.time_start,
                time_end=history.time_end,
                updated_at=history.updated_at,
            )
            for history in model.confirmation_history
        ]

        return RequestAggregate(
            id=RequestId(value=model.id),
            user_id=UserId(value=model.user_id),
            queue_id=QueueId(value=model.queue_id),
            purpose=model.purpose,
            status=RequestStatus(value=model.status),
            priority=RequestPriority(value=model.priority),
            created_at=model.created_at,
            updated_at=model.updated_at,
            preferred_datetime=preferred_datetime,
            confirmed_datetime=confirmed_datetime,
            status_history=status_history,
            confirmation_history=confirmation_history,
            archived=model.is_archived,
        )

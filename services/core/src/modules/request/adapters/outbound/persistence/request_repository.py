from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.request.domain.aggregates import Request as RequestAggregate, RequestId
from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.domain.value_objects import (
    QueueId,
    UserId,
    RequestDateTime,
    TimePeriod,
    RequestPriority,
    RequestStatus,
    RequestStatusHistoryItem as StatusHistoryVO,
    RequestConfirmationHistoryItem as ConfirmationHistoryVO,
)
from .models import (
    Request as RequestSchema,
    RequestStatusHistoryItem as RequestStatusHistoryItemSchema,
    RequestConfirmationHistoryItem as RequestConfirmationHistoryItemSchema,
    Queue as QueueSchema,
)


class RequestRepository(IRequestRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, request: RequestAggregate) -> None:
        request_model = self._request_to_orm(request)

        # Истории: перезаписываем коллекции (как в QueueRepository)
        request_model.status_history = [
            self._status_history_item_to_orm(item, request_model)
            for item in request.status_history
        ]
        request_model.confirmation_history = [
            self._confirmation_history_item_to_orm(item, request_model)
            for item in request.confirmation_history
        ]

        await self._session.merge(request_model)

    async def delete(self, request: RequestAggregate | RequestId) -> None:
        if isinstance(request, RequestAggregate):
            request_id = request.id.value
        else:
            request_id = request.value

        await self._session.execute(
            delete(RequestSchema).where(RequestSchema.id == request_id)
        )

    async def exists(self, request_id: RequestId) -> bool:
        result = await self._session.scalar(
            select(exists(RequestSchema.id)).where(RequestSchema.id == request_id.value)
        )
        return bool(result)

    async def find(self, request_id: RequestId) -> RequestAggregate | None:
        result = await self._session.execute(
            select(RequestSchema)
            .where(RequestSchema.id == request_id.value)
            .options(
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_history),
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._request_to_domain(model)

    # --------- ORM <-> domain маппинг ---------

    def _request_to_orm(self, request: RequestAggregate) -> RequestSchema:
        # Нужна локальная Queue-модель; предполагается, что она уже есть в БД
        queue_ref = QueueSchema(
            id=request.queue_id.value,
            owner_id=request.user_id.value,  # временный владелец, обновится из событий
            reception_time_start=request.preferred_datetime.time_period.start_time
            if request.preferred_datetime
            else request.confirmed_datetime.time_period.start_time
            if request.confirmed_datetime
            else TimePeriod(start_time=0, end_time=0).start_time,  # не попадёт в БД, если merge
            reception_time_end=request.preferred_datetime.time_period.end_time
            if request.preferred_datetime
            else request.confirmed_datetime.time_period.end_time
            if request.confirmed_datetime
            else TimePeriod(start_time=0, end_time=0).end_time,
        )

        preferred_date = (
            request.preferred_datetime.date if request.preferred_datetime else None
        )
        preferred_start = (
            request.preferred_datetime.time_period.start_time
            if request.preferred_datetime
            else None
        )
        preferred_end = (
            request.preferred_datetime.time_period.end_time
            if request.preferred_datetime
            else None
        )

        confirmed_date = (
            request.confirmed_datetime.date if request.confirmed_datetime else None
        )
        confirmed_start = (
            request.confirmed_datetime.time_period.start_time
            if request.confirmed_datetime
            else None
        )
        confirmed_end = (
            request.confirmed_datetime.time_period.end_time
            if request.confirmed_datetime
            else None
        )

        return RequestSchema(
            id=request.id.value,
            user_id=request.user_id.value,
            queue=queue_ref,
            purpose=request.purpose,
            preferred_date=preferred_date,
            preferred_time_start=preferred_start,
            preferred_time_end=preferred_end,
            confirmed_date=confirmed_date,
            confirmed_time_start=confirmed_start,
            confirmed_time_end=confirmed_end,
            is_archived=request.archived,
            priority=request.priority.value,
            status=request.status.value,
            created_at=request.created_at,
        )

    def _status_history_item_to_orm(
        self,
        item: StatusHistoryVO,
        request: RequestSchema,
    ) -> RequestStatusHistoryItemSchema:
        return RequestStatusHistoryItemSchema(
            request=request,
            status=item.status.value,
        )

    def _confirmation_history_item_to_orm(
        self,
        item: ConfirmationHistoryVO,
        request: RequestSchema,
    ) -> RequestConfirmationHistoryItemSchema:
        return RequestConfirmationHistoryItemSchema(
            request=request,
            date=item.date,
            time_start=item.time_start,
            time_end=item.time_end,
        )

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

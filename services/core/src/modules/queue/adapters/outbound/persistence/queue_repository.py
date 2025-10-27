from modules.queue.domain.ports.outbound import IQueueRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from sqlalchemy.orm import selectinload
from .models import Queue as QueueSchema
from .models import Request as RequestSchema
from .models import RequestStatusHistoryItem as RequestStatusHistoryItemSchema
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
    RequestStatusHistoryItem,
)
from modules.queue.domain.entities import Request


class QueueRepository(IQueueRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, queue: Queue) -> None:
        queue_model = self._queue_to_orm(queue)
        for req in queue.requests:
            request_schema = self._request_to_orm(req, queue_model)
            request_schema.status_history = [
                self._request_status_history_item_to_orm(history_item, request_schema)
                for history_item in req.status_history
            ]
            queue_model.requests.append(request_schema)
        await self._session.merge(queue_model)

    async def delete(self, queue: Queue | QueueId) -> None:
        if isinstance(queue, Queue):
            queue_id = queue.id.value
        else:
            queue_id = queue.value

        await self._session.execute(
            delete(QueueSchema).where(QueueSchema.id == queue_id)
        )

    async def exists(self, queue_id: QueueId) -> bool:
        result = await self._session.scalar(
            select(exists(QueueSchema.id)).where(QueueSchema.id == queue_id.value)
        )
        return bool(result)

    async def find(self, queue_id: QueueId) -> Queue | None:
        result = await self._session.execute(
            select(QueueSchema)
            .where(QueueSchema.id == queue_id.value)
            .options(
                selectinload(QueueSchema.requests).selectinload(
                    RequestSchema.status_history
                )
            )
        )
        queue_model = result.scalar_one_or_none()

        if queue_model is None:
            return None

        return self._queue_to_domain(queue_model)

    def _queue_to_orm(self, queue: Queue) -> QueueSchema:
        return QueueSchema(
            id=queue.id.value,
            owner_id=queue.owner_id.value,
            name=queue.name.value,
            description=queue.description.value,
            clean_up_period_days=queue.cleanup_period.value_days,
            reception_time_start=queue.reception_time.start_time,
            reception_time_end=queue.reception_time.end_time,
            is_active=queue.is_active.value,
        )

    def _request_to_orm(self, request: Request, queue: QueueSchema) -> RequestSchema:
        return RequestSchema(
            id=request.id.value,
            user_id=request.user_id.value,
            queue=queue,
            preferred_date=request.preferred_time.date,
            preferred_time_start=request.preferred_time.time_period.start_time,
            preferred_time_end=request.preferred_time.time_period.end_time,
            confirmed_date=(
                request.confirmed_time.date if request.confirmed_time else None
            ),
            confirmed_time_start=(
                request.confirmed_time.time_period.start_time
                if request.confirmed_time
                else None
            ),
            confirmed_time_end=(
                request.confirmed_time.time_period.end_time
                if request.confirmed_time
                else None
            ),
            archived=request.archived,
            created_at=request.created_at,
        )

    def _request_status_history_item_to_orm(
        self,
        request_status_history_item: RequestStatusHistoryItem,
        request: RequestSchema,
    ) -> RequestStatusHistoryItemSchema:
        return RequestStatusHistoryItemSchema(
            request=request,
            status=request_status_history_item.status.value,
        )

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
            requests=[
                self._request_to_domain(
                    request,
                    [
                        self._request_status_history_item_to_domain(status_history_item)
                        for status_history_item in request.status_history
                    ],
                )
                for request in model.requests
            ],
        )

    def _request_to_domain(
        self, model: RequestSchema, status_history: list[RequestStatusHistoryItem]
    ) -> Request:
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
            status_history=status_history,
        )

    def _request_status_history_item_to_domain(
        self, model: RequestStatusHistoryItemSchema
    ) -> RequestStatusHistoryItem:
        return RequestStatusHistoryItem(
            status=RequestStatus(value=model.status), updated_at=model.updated_at
        )

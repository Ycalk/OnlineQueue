from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.request.domain.aggregates import Request as RequestAggregate, RequestId
from modules.request.domain.entities import Queue
from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.domain.value_objects import (
    QueueId,
    UserId,
    RequestDatetime,
    TimePeriod,
    RequestPriority,
    RequestStatus,
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
    RequestStatusHistoryItem as RequestStatusHistoryItemSchema,
    RequestConfirmationDatetimeHistoryItem as RequestConfirmationHistoryItemSchema,
    RequestPriorityHistoryItem as RequestPriorityHistoryItemSchema,
    Comment as CommentSchema,
    Queue as QueueSchema,
)


class RequestRepository(IRequestRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, request: RequestAggregate) -> None:
        stmt = (
            select(RequestSchema)
            .options(
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.priority_history),
                selectinload(RequestSchema.confirmation_datetime_history),
                selectinload(RequestSchema.comments),
            )
            .where(RequestSchema.id == request.id.value)
        )
        result = await self._session.execute(stmt)
        request_model = self._to_orm(request, result.scalar_one_or_none())
        self._session.add(request_model)

        await self._session.flush()

    async def exists(self, request_id: RequestId) -> bool:
        stmt = select(RequestSchema.id).where(RequestSchema.id == request_id.value)
        result = await self._session.execute(stmt)
        return result.first() is not None

    async def find_by_id(self, request_id: RequestId) -> RequestAggregate | None:
        stmt = (
            select(RequestSchema)
            .options(
                selectinload(RequestSchema.queue),
                selectinload(RequestSchema.status_history),
                selectinload(RequestSchema.confirmation_datetime_history),
                selectinload(RequestSchema.priority_history),
                selectinload(RequestSchema.comments),
            )
            .where(RequestSchema.id == request_id.value)
        )
        result = await self._session.execute(stmt)
        request_model = result.scalar_one_or_none()

        if not request_model:
            return None

        return self._to_domain(request_model)

    async def find_queue_by_id(self, queue_id: QueueId) -> Queue | None:
        stmt = select(QueueSchema).where(QueueSchema.id == queue_id.value)
        result = await self._session.execute(stmt)
        queue_model = result.scalar_one_or_none()

        if not queue_model:
            return None

        return self._queue_to_domain(queue_model)

    async def save_queue(self, queue: Queue) -> None:
        queue_model = self._queue_to_orm(queue)
        self._session.add(queue_model)
        await self._session.flush()

    def _to_orm(
        self, aggregate: RequestAggregate, schema: RequestSchema | None = None
    ) -> RequestSchema:
        result = RequestSchema(
            id=aggregate.id.value,
            user_id=aggregate.user_id.value,
            queue=self._queue_to_orm(aggregate.queue),
            purpose=aggregate.purpose.value,
            preferred_date=aggregate.preferred_datetime.date,
            preferred_time_start=aggregate.preferred_datetime.time_period.start_time,
            preferred_time_end=aggregate.preferred_datetime.time_period.end_time,
            archived=aggregate.archived,
        )
        if schema is None:
            result.status_history = [
                RequestStatusHistoryItemSchema(request=result, status=item.status.value)
                for item in aggregate.status_history
            ]

            result.priority_history = [
                RequestPriorityHistoryItemSchema(
                    request=result, priority=item.priority.value
                )
                for item in aggregate.priority_history
            ]

            result.confirmation_datetime_history = [
                RequestConfirmationHistoryItemSchema(
                    request=result,
                    date=item.confirmation_datetime.date
                    if item.confirmation_datetime
                    else None,
                    time_start=item.confirmation_datetime.time_period.start_time
                    if item.confirmation_datetime
                    else None,
                    time_end=item.confirmation_datetime.time_period.end_time
                    if item.confirmation_datetime
                    else None,
                )
                for item in aggregate.confirmation_datetime_history
            ]

            result.comments = [
                CommentSchema(request=result, author=item.author.value, text=item.text)
                for item in aggregate.comments
            ]
        else:
            result.status_history = schema.status_history
            result.priority_history = schema.priority_history
            result.confirmation_datetime_history = schema.confirmation_datetime_history
            result.comments = schema.comments

            for status_history_item in aggregate.status_history[
                len(result.status_history) :
            ]:
                result.status_history.append(
                    RequestStatusHistoryItemSchema(
                        request=result,
                        status=status_history_item.status.value,
                        occurred_at=status_history_item.occurred_at,
                    )
                )
            for priority_history_item in aggregate.priority_history[
                len(result.priority_history) :
            ]:
                result.priority_history.append(
                    RequestPriorityHistoryItemSchema(
                        request=result,
                        priority=priority_history_item.priority.value,
                        occurred_at=priority_history_item.occurred_at,
                    )
                )
            for confirmation_history_item in aggregate.confirmation_datetime_history[
                len(result.confirmation_datetime_history) :
            ]:
                result.confirmation_datetime_history.append(
                    RequestConfirmationHistoryItemSchema(
                        request=result,
                        date=confirmation_history_item.confirmation_datetime.date
                        if confirmation_history_item.confirmation_datetime
                        else None,
                        time_start=confirmation_history_item.confirmation_datetime.time_period.start_time
                        if confirmation_history_item.confirmation_datetime
                        else None,
                        time_end=confirmation_history_item.confirmation_datetime.time_period.end_time
                        if confirmation_history_item.confirmation_datetime
                        else None,
                        occurred_at=confirmation_history_item.occurred_at,
                    )
                )
            for comment in aggregate.comments[len(result.comments) :]:
                result.comments.append(
                    CommentSchema(
                        request=result,
                        author=comment.author.value,
                        text=comment.text,
                        created_at=comment.created_at,
                    )
                )

        return result

    def _queue_to_orm(self, entity: Queue) -> QueueSchema:
        return QueueSchema(
            id=entity.id.value,
            owner_id=entity.owner_id.value,
            reception_time_start=entity.reception_time.start_time,
            reception_time_end=entity.reception_time.end_time,
            is_active=entity.is_active.value,
        )

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
                )
                if item.date is not None
                and item.time_start is not None
                and item.time_end is not None
                else None,
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

        request = RequestAggregate(
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
        return request

    def _queue_to_domain(self, model: QueueSchema) -> Queue:
        return Queue(
            id=QueueId(value=model.id),
            owner_id=UserId(value=model.owner_id),
            is_active=IsActive(value=model.is_active),
            reception_time=TimePeriod(
                start_time=model.reception_time_start, end_time=model.reception_time_end
            ),
        )

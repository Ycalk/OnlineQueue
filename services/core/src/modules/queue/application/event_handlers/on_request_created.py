from logging import getLogger

from shared.building_blocks.event import IEventHandler

from modules.queue.domain.ports.outbound import IQueueRepository
from modules.queue.domain.aggregates import QueueId
from modules.queue.domain.entities import Request
from modules.queue.domain.value_objects import (
    RequestId,
    UserId,
    RequestDateTime,
    TimePeriod,
    RequestStatus,
    RequestPriority,
)
from modules.queue.application.errors import QueueNotFoundError

from modules.request.domain.events.request_created import RequestCreated


class OnRequestCreated(IEventHandler[RequestCreated]):
    def __init__(self, queue_repository: IQueueRepository):
        self._queue_repository = queue_repository
        self._logger = getLogger("event_handler.on_request_created")

    async def __call__(self, event: RequestCreated) -> None:
        self._logger.info(
            f"Handling request created event for request with id {event.request_id}"
        )
        queue = await self._queue_repository.find(QueueId(value=event.queue_id))
        if queue is None:
            self._logger.error(
                f"Queue with id {event.queue_id} not found: event not handled",
                exc_info=True,
            )
            raise QueueNotFoundError(f"Queue with id {event.queue_id} not found")

        queue.on_request_created(
            Request(
                id=RequestId(value=event.request_id),
                user_id=UserId(value=event.user_id),
                preferred_time=RequestDateTime(
                    date=event.preferred_date,
                    time_period=TimePeriod(
                        start_time=event.preferred_time_start,
                        end_time=event.preferred_time_end,
                    ),
                ),
                status=RequestStatus(event.status.value),
                priority=RequestPriority(event.priority.value),
                archived=False,
                created_at=event.occurred_at,
            )
        )
        await self._queue_repository.save(queue)
        self._logger.info(f"Event handled for request with id {event.request_id}")

    @classmethod
    def event_type(cls) -> type[RequestCreated]:
        return RequestCreated

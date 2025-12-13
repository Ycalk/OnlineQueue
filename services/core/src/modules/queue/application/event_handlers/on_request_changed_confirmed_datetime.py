from shared.building_blocks.event import IEventHandler, IEventPublisher

from modules.queue.domain.ports.outbound import IQueueRepository
from modules.queue.domain.value_objects import (
    RequestId,
    RequestDateTime,
    TimePeriod,
)
from modules.queue.application.errors import QueueNotFoundError

from modules.request.domain.events.request_changed_confirmed_datetime import (
    RequestChangedConfirmedDatetime,
)


class OnRequestChangedConfirmedDatetime(IEventHandler[RequestChangedConfirmedDatetime]):
    def __init__(
        self, queue_repository: IQueueRepository, event_publisher: IEventPublisher
    ):
        self._queue_repository = queue_repository
        self._event_publisher = event_publisher

    async def __call__(self, event: RequestChangedConfirmedDatetime) -> None:
        queue = await self._queue_repository.find_by_request_id(
            RequestId(value=event.request_id)
        )
        if queue is None:
            raise QueueNotFoundError(
                f"Queue for request with id {event.request_id} not found"
            )

        queue.on_change_request_confirmed_time(
            RequestId(value=event.request_id),
            RequestDateTime(
                date=event.new_confirmed_date,
                time_period=TimePeriod(
                    start_time=event.new_confirmed_time_start,
                    end_time=event.new_confirmed_time_end,
                ),
            ),
        )
        await self._queue_repository.save(queue)
        for queue_event in queue.events:
            await self._event_publisher.publish(queue_event)

    @classmethod
    def event_type(cls) -> type[RequestChangedConfirmedDatetime]:
        return RequestChangedConfirmedDatetime

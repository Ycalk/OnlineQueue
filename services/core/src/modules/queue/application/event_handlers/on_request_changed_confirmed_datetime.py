from logging import getLogger

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
        self,
        queue_repository: IQueueRepository,
        event_publisher: IEventPublisher,
    ):
        self._queue_repository = queue_repository
        self._event_publisher = event_publisher
        self._logger = getLogger("event_handler.on_request_changed_confirmed_datetime")

    async def __call__(self, event: RequestChangedConfirmedDatetime) -> None:
        self._logger.info(
            f"Handling request changed confirmed datetime event for request with id {event.request_id}"
        )
        queue = await self._queue_repository.find_by_request_id(
            RequestId(value=event.request_id)
        )
        if queue is None:
            self._logger.error(
                f"Queue for request with id {event.request_id} not found: event not handled",
                exc_info=True,
            )
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
        self._logger.info(
            f"Event handed for request with id {event.request_id}. Publishing {len(queue.events)} queue events to event bus"
        )
        for queue_event in queue.events:
            await self._event_publisher.publish(queue_event)

        self._logger.info(
            f"Request with id {event.request_id} confirmed datetime changed successfully: event handled"
        )

    @classmethod
    def event_type(cls) -> type[RequestChangedConfirmedDatetime]:
        return RequestChangedConfirmedDatetime

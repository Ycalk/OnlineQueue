from logging import getLogger

from shared.building_blocks.event import IEventHandler

from modules.queue.domain.ports.outbound import IQueueRepository
from modules.queue.domain.value_objects import RequestId
from modules.queue.application.errors import QueueNotFoundError

from modules.request.domain.events.request_rejected import (
    RequestRejected,
)


class OnRequestRejected(IEventHandler[RequestRejected]):
    def __init__(self, queue_repository: IQueueRepository):
        self._queue_repository = queue_repository
        self._logger = getLogger("event_handler.on_request_rejected")

    async def __call__(self, event: RequestRejected) -> None:
        self._logger.info(
            f"Handling request rejected event for request with id {event.request_id}"
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

        queue.on_request_rejected(
            RequestId(value=event.request_id),
        )
        await self._queue_repository.save(queue)
        self._logger.info(f"Event handed for request with id {event.request_id}")

    @classmethod
    def event_type(cls) -> type[RequestRejected]:
        return RequestRejected

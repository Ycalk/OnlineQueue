from shared.building_blocks.event import IEventHandler

from modules.queue.domain.ports.outbound import IQueueRepository
from modules.queue.domain.value_objects import RequestId, RequestPriority
from modules.queue.application.errors import QueueNotFoundError

from modules.request.domain.events.request_changed_priority import (
    RequestChangedPriority,
)


class OnRequestChangedPriority(IEventHandler[RequestChangedPriority]):
    def __init__(self, queue_repository: IQueueRepository):
        self._queue_repository = queue_repository

    async def __call__(self, event: RequestChangedPriority) -> None:
        queue = await self._queue_repository.find_by_request_id(
            RequestId(value=event.request_id)
        )
        if queue is None:
            raise QueueNotFoundError(
                f"Queue for request with id {event.request_id} not found"
            )

        queue.on_change_request_priority(
            RequestId(value=event.request_id),
            RequestPriority(event.new_priority.value),
        )
        await self._queue_repository.save(queue)

    @classmethod
    def event_type(cls) -> type[RequestChangedPriority]:
        return RequestChangedPriority

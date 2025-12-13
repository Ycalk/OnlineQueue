from shared.building_blocks.event import IEventHandler

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.application.errors import QueueNotFoundError
from modules.request.domain.value_objects import QueueId

from modules.queue.domain.events.queue_activated import QueueActivated


class OnQueueActivated(IEventHandler[QueueActivated]):
    def __init__(self, request_repository: IRequestRepository):
        self._request_repository = request_repository

    async def __call__(self, event: QueueActivated) -> None:
        queue = await self._request_repository.find_queue_by_id(
            QueueId(value=event.queue_id)
        )
        if queue is None:
            raise QueueNotFoundError(f"Queue with id {event.queue_id} not found")

        queue.activate()

        await self._request_repository.save_queue(queue)

    @classmethod
    def event_type(cls) -> type[QueueActivated]:
        return QueueActivated

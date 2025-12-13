from logging import getLogger

from shared.building_blocks.event import IEventHandler

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.application.errors import QueueNotFoundError
from modules.request.domain.value_objects import QueueId

from modules.queue.domain.events.queue_activated import QueueActivated


class OnQueueActivated(IEventHandler[QueueActivated]):
    def __init__(self, request_repository: IRequestRepository):
        self._request_repository = request_repository
        self._logger = getLogger("event_handler.on_queue_activated")

    async def __call__(self, event: QueueActivated) -> None:
        self._logger.info(
            f"Handling queue activated event for queue with id {event.queue_id}"
        )
        queue = await self._request_repository.find_queue_by_id(
            QueueId(value=event.queue_id)
        )
        if queue is None:
            self._logger.error(
                f"Queue with id {event.queue_id} not found: event not handled",
                exc_info=True,
            )
            raise QueueNotFoundError(f"Queue with id {event.queue_id} not found")

        queue.activate()

        await self._request_repository.save_queue(queue)
        self._logger.info(
            f"Queue with id {event.queue_id} activated successfully: event handled"
        )

    @classmethod
    def event_type(cls) -> type[QueueActivated]:
        return QueueActivated

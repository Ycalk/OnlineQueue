from logging import getLogger

from shared.building_blocks.event import IEventHandler

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.application.errors import QueueNotFoundError
from modules.request.domain.value_objects import QueueId

from modules.queue.domain.events.queue_deactivated import QueueDeactivated


class OnQueueDeactivated(IEventHandler[QueueDeactivated]):
    def __init__(self, request_repository: IRequestRepository):
        self._request_repository = request_repository
        self._logger = getLogger("event_handler.on_queue_deactivated")

    async def __call__(self, event: QueueDeactivated) -> None:
        self._logger.info(
            f"Handling queue deactivated event for queue with id {event.queue_id}"
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

        queue.deactivate()

        await self._request_repository.save_queue(queue)
        self._logger.info(
            f"Queue with id {event.queue_id} deactivated successfully: event handled"
        )

    @classmethod
    def event_type(cls) -> type[QueueDeactivated]:
        return QueueDeactivated

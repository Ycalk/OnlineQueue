from abc import ABC
from shared.building_blocks.event import IEventPublisher
from modules.queue.domain.ports.outbound import IQueueRepository
from shared.building_blocks.use_case import ApplicationUseCase
from modules.queue.domain.aggregates import Queue, QueueId
from modules.queue.domain.value_objects import UserId
from modules.queue.application.errors import QueueNotFoundError, NoRightsError


class QueueOwnerUseCase(ApplicationUseCase, ABC):
    """Base class для use cases требующих права владельца"""

    def __init__(
        self, event_publisher: IEventPublisher, queue_repository: IQueueRepository
    ):
        super().__init__(event_publisher)
        self._queue_repository = queue_repository

    async def _load_and_check_owner(
        self, queue_id: QueueId, requester: UserId
    ) -> Queue:
        queue = await self._queue_repository.find(queue_id)

        if queue is None:
            raise QueueNotFoundError(f"Queue with id {queue_id} not found")

        if queue.owner_id != requester:
            raise NoRightsError(f"User {requester} has no rights to change queue")

        return queue

from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase

from modules.queue.domain.commands import DeactivateQueue as DeactivateQueueCommand
from modules.queue.domain.ports.inbound.use_cases import IDeactivateQueue
from modules.queue.domain.ports.outbound import IQueueRepository
from modules.queue.application.errors import QueueNotFoundError, NoRightsError


class DeactivateQueue(ApplicationUseCase, IDeactivateQueue):
    def __init__(
        self, event_publisher: IEventPublisher, queue_repository: IQueueRepository
    ):
        super().__init__(event_publisher)
        self._queue_repository = queue_repository

    async def __call__(self, command: DeactivateQueueCommand) -> None:
        queue = await self._queue_repository.find(command.queue_id)
        if queue is None:
            raise QueueNotFoundError(f"Queue with id {command.queue_id} not found")
        if queue.owner_id != command.requester:
            raise NoRightsError(
                f"User {command.requester} has no rights to change queue"
            )

        queue.deactivate()
        await self._queue_repository.save(queue)

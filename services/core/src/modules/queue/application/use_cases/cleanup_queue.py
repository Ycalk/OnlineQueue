from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import CleanupQueue as CleanupQueueCommand
from modules.queue.domain.ports.inbound.use_cases import ICleanupQueue


class CleanupQueue(QueueOwnerUseCase, ICleanupQueue):
    async def __call__(self, command: CleanupQueueCommand) -> None:
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.cleanup()
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

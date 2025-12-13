from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import CleanupQueue as CleanupQueueCommand
from modules.queue.domain.ports.inbound.use_cases import ICleanupQueue


class CleanupQueue(QueueOwnerUseCase, ICleanupQueue):
    async def __call__(self, command: CleanupQueueCommand) -> None:
        self._logger.info(f"Cleaning up queue with id {command.queue_id.value}")
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.cleanup()
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

        await self._queue_repository.commit()
        self._logger.info(
            f"Queue with id {command.queue_id.value} cleaned up successfully"
        )

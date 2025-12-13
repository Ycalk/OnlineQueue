from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import DeactivateQueue as DeactivateQueueCommand
from modules.queue.domain.ports.inbound.use_cases import IDeactivateQueue


class DeactivateQueue(QueueOwnerUseCase, IDeactivateQueue):
    async def __call__(self, command: DeactivateQueueCommand) -> None:
        self._logger.info(f"Deactivating queue with id {command.queue_id.value}")
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.deactivate()
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

        await self._queue_repository.commit()
        self._logger.info(f"Queue with id {queue.id.value} deactivated successfully")

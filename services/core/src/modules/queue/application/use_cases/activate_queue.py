from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import ActivateQueue as ActivateQueueCommand
from modules.queue.domain.ports.inbound.use_cases import IActivateQueue


class ActivateQueue(QueueOwnerUseCase, IActivateQueue):
    async def __call__(self, command: ActivateQueueCommand) -> None:
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.activate()
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

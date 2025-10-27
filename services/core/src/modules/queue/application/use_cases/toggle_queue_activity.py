from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import (
    ToggleQueueActivity as ToggleQueueActivityCommand,
)
from modules.queue.domain.ports.inbound.use_cases import IToggleQueueActivity


class ToggleQueueActivity(QueueOwnerUseCase, IToggleQueueActivity):
    async def __call__(self, command: ToggleQueueActivityCommand) -> None:
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        if queue.is_active:
            queue.deactivate()
        else:
            queue.activate()
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

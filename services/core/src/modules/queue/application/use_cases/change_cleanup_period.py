from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import (
    ChangeCleanupPeriod as ChangeCleanupPeriodCommand,
)
from modules.queue.domain.ports.inbound.use_cases import IChangeCleanupPeriod


class ChangeCleanupPeriod(QueueOwnerUseCase, IChangeCleanupPeriod):
    async def __call__(self, command: ChangeCleanupPeriodCommand) -> None:
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.change_cleanup_period(command.new_cleanup_period)
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

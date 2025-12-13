from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import (
    ChangeCleanupPeriod as ChangeCleanupPeriodCommand,
)
from modules.queue.domain.ports.inbound.use_cases import IChangeCleanupPeriod


class ChangeCleanupPeriod(QueueOwnerUseCase, IChangeCleanupPeriod):
    async def __call__(self, command: ChangeCleanupPeriodCommand) -> None:
        self._logger.info(
            f"Changing cleanup period for queue with id {command.queue_id.value}"
        )
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.change_cleanup_period(command.new_cleanup_period)
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

        await self._queue_repository.commit()
        self._logger.info(
            f"Cleanup period for queue with id {command.queue_id.value} changed successfully"
        )

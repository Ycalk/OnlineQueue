from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import ChangeName as ChangeNameCommand
from modules.queue.domain.ports.inbound.use_cases import IChangeName


class ChangeName(QueueOwnerUseCase, IChangeName):
    async def __call__(self, command: ChangeNameCommand) -> None:
        self._logger.info(f"Changing name for queue with id {command.queue_id.value}")
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.change_name(command.new_name)
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

        await self._queue_repository.commit()
        self._logger.info(
            f"Name for queue with id {command.queue_id.value} changed successfully"
        )

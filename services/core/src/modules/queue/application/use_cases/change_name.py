from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import ChangeName as ChangeNameCommand
from modules.queue.domain.ports.inbound.use_cases import IChangeName


class ChangeName(QueueOwnerUseCase, IChangeName):
    async def __call__(self, command: ChangeNameCommand) -> None:
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.change_name(command.new_name)
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

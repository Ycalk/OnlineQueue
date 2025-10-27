from ._base import QueueOwnerUseCase
from modules.queue.domain.commands import (
    ChangeDescription as ChangeDescriptionCommand,
)
from modules.queue.domain.ports.inbound.use_cases import IChangeDescription


class ChangeDescription(QueueOwnerUseCase, IChangeDescription):
    async def __call__(self, command: ChangeDescriptionCommand) -> None:
        queue = await self._load_and_check_owner(command.queue_id, command.requester)

        queue.change_description(command.new_description)
        await self._queue_repository.save(queue)
        await self._publish_events(queue)

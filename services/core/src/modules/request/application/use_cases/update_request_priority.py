from ._base import RequestOwnerUseCase
from modules.request.domain.commands import (
    UpdateRequestPriority as UpdateRequestPriorityCommand,
)
from modules.request.domain.ports.inbound import IUpdateRequestPriority


class UpdateRequestPriority(RequestOwnerUseCase, IUpdateRequestPriority):
    async def __call__(self, command: UpdateRequestPriorityCommand) -> None:
        request = await self._load_and_check_owner(
            command.request_id,
            command.requester,
        )

        # Можно вынести в доменный метод change_priority, если понадобится
        request.priority = command.new_priority

        await self._request_repository.save(request)
        await self._publish_events(request)

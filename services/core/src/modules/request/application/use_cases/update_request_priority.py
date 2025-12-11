from ._base import BaseRequestUseCase
from modules.request.domain.commands import (
    UpdateRequestPriority as UpdateRequestPriorityCommand,
)
from modules.request.domain.ports.inbound import IUpdateRequestPriority


class UpdateRequestPriority(BaseRequestUseCase, IUpdateRequestPriority):
    async def __call__(self, command: UpdateRequestPriorityCommand) -> None:
        request = await self._load_and_check_queue_owner(
            command.request_id,
            command.requester,
        )

        request.update_priority(command.new_priority)

        await self._request_repository.save(request)
        await self._publish_events(request)

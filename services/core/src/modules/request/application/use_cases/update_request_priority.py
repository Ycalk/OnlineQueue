from ._base import BaseRequestUseCase
from modules.request.domain.commands import (
    UpdateRequestPriority as UpdateRequestPriorityCommand,
)
from modules.request.domain.ports.inbound import IUpdateRequestPriority


class UpdateRequestPriority(BaseRequestUseCase, IUpdateRequestPriority):
    async def __call__(self, command: UpdateRequestPriorityCommand) -> None:
        self._logger.info(
            f"Updating priority for request with id {command.request_id.value} to {command.new_priority.value}"
        )
        request = await self._load_and_check_queue_owner(
            command.request_id,
            command.requester,
        )

        request.update_priority(command.new_priority)

        await self._request_repository.save(request)

        await self._publish_events(request)

        await self._request_repository.commit()
        self._logger.info(
            f"Request with id {request.id.value} priority updated to {command.new_priority.value} successfully"
        )

from ._base import BaseRequestUseCase
from modules.request.domain.commands import (
    UpdateRequestConfirmationDatetime as UpdateRequestConfirmationDatetimeCommand,
)
from modules.request.domain.ports.inbound import IUpdateRequestConfirmationDatetime


class UpdateRequestConfirmationDatetime(
    BaseRequestUseCase, IUpdateRequestConfirmationDatetime
):
    async def __call__(self, command: UpdateRequestConfirmationDatetimeCommand) -> None:
        request = await self._load_and_check_queue_owner(
            command.request_id,
            command.requester,
        )

        request.update_confirmation_datetime(command.new_confirmed_datetime)

        await self._request_repository.save(request)
        await self._publish_events(request)

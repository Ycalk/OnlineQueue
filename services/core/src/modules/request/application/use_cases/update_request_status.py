from ._base import RequestOwnerUseCase
from modules.request.domain.commands import (
    UpdateRequestStatus as UpdateRequestStatusCommand,
)
from modules.request.domain.ports.inbound import IUpdateRequestStatus
from modules.request.domain.value_objects import RequestStatus


class UpdateRequestStatus(RequestOwnerUseCase, IUpdateRequestStatus):
    async def __call__(self, command: UpdateRequestStatusCommand) -> None:
        request = await self._load_and_check_owner(
            command.request_id,
            command.requester,
        )

        if command.new_status is RequestStatus.ACCEPTED:
            request.accept()  # без назначения времени
        elif command.new_status is RequestStatus.REJECTED:
            request.reject()
        elif command.new_status is RequestStatus.PENDING:
            # Явного «возврата в очередь» не делаем — можно добавить
            # отдельный доменный метод, если тимлид захочет такой сценарий.
            return

        await self._request_repository.save(request)
        await self._publish_events(request)

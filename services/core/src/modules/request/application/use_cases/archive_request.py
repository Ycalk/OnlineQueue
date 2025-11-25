from ._base import RequestOwnerUseCase
from modules.request.domain.commands import ArchiveRequest as ArchiveRequestCommand
from modules.request.domain.ports.inbound import IArchiveRequest


class ArchiveRequest(RequestOwnerUseCase, IArchiveRequest):
    async def __call__(self, command: ArchiveRequestCommand) -> None:
        request = await self._load_and_check_owner(
            command.request_id,
            command.requester,
        )

        request.archive()

        await self._request_repository.save(request)
        await self._publish_events(request)

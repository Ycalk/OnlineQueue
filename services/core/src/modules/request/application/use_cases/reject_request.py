from ._base import BaseRequestUseCase
from modules.request.domain.commands import (
    RejectRequest as RejectRequestCommand,
)
from modules.request.domain.ports.inbound import IRejectRequest
from modules.request.application.errors import RequestNotFoundError, NoRightsError


class RejectRequest(BaseRequestUseCase, IRejectRequest):
    async def __call__(self, command: RejectRequestCommand) -> None:
        self._logger.info(f"Rejecting request with id {command.request_id.value}")
        request = await self._request_repository.find_by_id(command.request_id)

        if request is None:
            self._logger.info(
                f"Request with id {command.request_id.value} not found: request not rejected"
            )
            raise RequestNotFoundError(
                f"Request with id {command.request_id} not found"
            )

        if (
            request.queue.owner_id != command.requester
            and request.user_id != command.requester
        ):
            self._logger.info(
                (
                    f"User {command.requester.value} has no rights "
                    f"to reject request {command.request_id}: request not rejected"
                )
            )
            raise NoRightsError(
                f"User {command.requester.value} has no rights to reject request {command.request_id}"
            )

        request.reject()

        await self._request_repository.save(request)

        await self._publish_events(request)

        await self._request_repository.commit()
        self._logger.info(f"Request with id {request.id.value} rejected successfully")

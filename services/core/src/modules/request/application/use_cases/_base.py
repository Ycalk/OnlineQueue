from abc import ABC

from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.domain.aggregates import Request, RequestId
from modules.request.domain.value_objects import UserId
from modules.request.application.errors import RequestNotFoundError, NoRightsError


class BaseRequestUseCase(ApplicationUseCase, ABC):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ):
        super().__init__(event_publisher)
        self._request_repository = request_repository

    async def _load_and_check_queue_owner(
        self,
        request_id: RequestId,
        requester: UserId,
    ) -> Request:
        request = await self._request_repository.find_by_id(request_id)

        if request is None:
            raise RequestNotFoundError(f"Request with id {request_id} not found")

        if request.queue.owner_id != requester:
            raise NoRightsError(
                f"User {requester.value} has no rights to change request {request_id}"
            )

        return request

    async def _load_and_check_requester(
        self,
        request_id: RequestId,
        requester: UserId,
    ) -> Request:
        request = await self._request_repository.find_by_id(request_id)

        if request is None:
            raise RequestNotFoundError(f"Request with id {request_id} not found")

        if request.user_id != requester:
            raise NoRightsError(
                f"User {requester.value} has no rights to change request {request_id}"
            )

        return request

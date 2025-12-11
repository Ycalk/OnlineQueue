from modules.request.application.ports.inbound.queries import IGetUserRequests
from modules.request.application.dto import (
    Request,
    GetUserRequests as GetUserRequestsQuery,
)
from ._base import BaseRequestQuery


class GetUserRequests(BaseRequestQuery, IGetUserRequests):
    async def __call__(self, request: GetUserRequestsQuery) -> list[Request]:
        requests = await self._request_reader.get_by_user_id(
            request.user_id, request.skip, request.limit
        )
        return [self._request_to_dto(request) for request in requests]

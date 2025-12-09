from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.application.ports.inbound.queries import IGetUserRequests
from modules.request.application.dto import Request, GetUserRequests as GetUserRequestsDto
from ._mapping import map_request


class GetUserRequests(IGetUserRequests):
    def __init__(self, request_reader: IRequestReader):
        self._request_reader = request_reader

    async def __call__(self, request: GetUserRequestsDto) -> list[Request]:
        requests = await self._request_reader.find_by_user_id(request.user_id)
        return [map_request(r) for r in requests]

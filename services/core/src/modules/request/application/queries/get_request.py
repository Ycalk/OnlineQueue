from uuid import UUID

from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.application.ports.inbound.queries import IGetRequest
from modules.request.application.dto import Request
from modules.request.application.errors import RequestNotFoundError
from modules.request.application.queries._mapping import map_request


class GetRequest(IGetRequest):
    def __init__(self, request_reader: IRequestReader):
        self._request_reader = request_reader

    async def __call__(self, request: UUID) -> Request:
        req = await self._request_reader.find_by_id(request)
        if req is None:
            raise RequestNotFoundError(f"Request with id {request} not found")
        return map_request(req)

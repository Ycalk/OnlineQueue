from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.application.ports.inbound.queries import IGetRequestList
from modules.request.application.dto import Request, GetRequestList as GetRequestListDto
from modules.request.application.queries._mapping import map_request


class GetRequestList(IGetRequestList):
    def __init__(self, request_reader: IRequestReader):
        self._request_reader = request_reader

    async def __call__(self, request: GetRequestListDto) -> list[Request]:
        requests = await self._request_reader.get_many(request.skip, request.limit)
        return [map_request(r) for r in requests]

from uuid import UUID

from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.application.ports.inbound.queries import IGetQueueRequests
from modules.request.application.dto import Request
from modules.request.application.queries._mapping import map_request


class GetQueueRequests(IGetQueueRequests):
    def __init__(self, request_reader: IRequestReader):
        self._request_reader = request_reader

    async def __call__(self, request: UUID) -> list[Request]:
        requests = await self._request_reader.find_by_queue_id(request)
        return [map_request(r) for r in requests]

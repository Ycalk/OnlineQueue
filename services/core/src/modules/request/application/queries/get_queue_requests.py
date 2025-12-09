from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.application.ports.inbound.queries import IGetQueueRequests
from modules.request.application.dto import Request, GetQueueRequests as GetQueueRequestsDto
from ._mapping import map_request


class GetQueueRequests(IGetQueueRequests):
    def __init__(self, request_reader: IRequestReader):
        self._request_reader = request_reader

    async def __call__(self, request: GetQueueRequestsDto) -> list[Request]:
        requests = await self._request_reader.find_by_queue_id(request.queue_id)
        return [map_request(r) for r in requests]

from uuid import UUID

from modules.request.application.ports.inbound.queries import IGetQueueOwnerRequests
from modules.request.application.dto import Request
from modules.request.application.queries._base import BaseRequestQuery


class GetQueueOwnerRequests(BaseRequestQuery, IGetQueueOwnerRequests):
    async def __call__(self, request: UUID) -> list[Request]:
        requests = await self._request_reader.get_by_queue_owner_id(request)
        return [self._request_to_dto(request) for request in requests]

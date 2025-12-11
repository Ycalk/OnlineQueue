from modules.request.application.ports.inbound.queries import IGetQueueRequests
from modules.request.application.dto import (
    Request,
    GetQueueRequests as GetQueueRequestsQuery,
)
from modules.request.application.errors import NoRightsError, QueueNotFoundError
from ._base import BaseRequestQuery


class GetQueueRequests(BaseRequestQuery, IGetQueueRequests):
    async def __call__(self, request: GetQueueRequestsQuery) -> list[Request]:
        queue = await self._request_reader.find_queue_by_id(request.queue_id)
        if queue is None:
            raise QueueNotFoundError(f"Queue with id {request.queue_id} not found")

        if queue.owner_id.value != request.requester_id:
            raise NoRightsError("You have no rights to get requests for this queue")

        requests = await self._request_reader.get_by_queue_id(request.queue_id)

        return [self._request_to_dto(request) for request in requests]

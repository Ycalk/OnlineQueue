from modules.request.application.ports.inbound.queries import IGetRequest
from modules.request.application.dto import Request, GetRequest as GetRequestQuery
from modules.request.application.errors import RequestNotFoundError, NoRightsError
from modules.request.application.queries._base import BaseRequestQuery


class GetRequest(BaseRequestQuery, IGetRequest):
    async def __call__(self, query: GetRequestQuery) -> Request:
        request = await self._request_reader.find_by_id(query.request_id)
        if request is None:
            raise RequestNotFoundError(f"Request with id {request} not found")

        if (
            request.queue.owner_id.value != query.requester_id
            and request.user_id.value != query.requester_id
        ):
            raise NoRightsError("You have no rights to get this request")

        return self._request_to_dto(request)

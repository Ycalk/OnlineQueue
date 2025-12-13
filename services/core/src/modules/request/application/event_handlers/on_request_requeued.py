from shared.building_blocks.event import IEventHandler

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.application.errors import RequestNotFoundError
from modules.request.domain.aggregates import RequestId

from modules.queue.domain.events.request_requeued import RequestRequeued


class OnRequestRequeued(IEventHandler[RequestRequeued]):
    def __init__(self, request_repository: IRequestRepository):
        self._request_repository = request_repository

    async def __call__(self, event: RequestRequeued) -> None:
        request = await self._request_repository.find_by_id(
            RequestId(value=event.request_id)
        )
        if request is None:
            raise RequestNotFoundError(f"Request with id {event.request_id} not found")

        request.on_requeued()

        await self._request_repository.save(request)

    @classmethod
    def event_type(cls) -> type[RequestRequeued]:
        return RequestRequeued

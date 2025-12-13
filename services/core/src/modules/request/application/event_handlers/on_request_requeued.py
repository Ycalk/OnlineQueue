from logging import getLogger

from shared.building_blocks.event import IEventHandler

from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.application.errors import RequestNotFoundError
from modules.request.domain.aggregates import RequestId

from modules.queue.domain.events.request_requeued import RequestRequeued


class OnRequestRequeued(IEventHandler[RequestRequeued]):
    def __init__(self, request_repository: IRequestRepository):
        self._request_repository = request_repository
        self._logger = getLogger("event_handler.on_request_requeued")

    async def __call__(self, event: RequestRequeued) -> None:
        self._logger.info(
            f"Handling request requeued event for request with id {event.request_id}"
        )
        request = await self._request_repository.find_by_id(
            RequestId(value=event.request_id)
        )
        if request is None:
            self._logger.error(
                f"Request with id {event.request_id} not found: event not handled",
                exc_info=True,
            )
            raise RequestNotFoundError(f"Request with id {event.request_id} not found")

        request.on_requeued()

        await self._request_repository.save(request)
        self._logger.info(
            f"Request with id {event.request_id} requeued successfully: event handled"
        )

    @classmethod
    def event_type(cls) -> type[RequestRequeued]:
        return RequestRequeued

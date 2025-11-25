from datetime import date, time

from shared.building_blocks.event import IEventPublisher
from shared.building_blocks.use_case import ApplicationUseCase

from modules.request.domain.commands import CreateRequest as CreateRequestCommand
from modules.request.domain.ports.inbound import ICreateRequest
from modules.request.domain.aggregates import Request
from modules.request.domain.ports.outbound import IRequestRepository
from modules.request.domain.value_objects import (
    RequestDateTime,
    TimePeriod,
    RequestPriority,
)


class CreateRequest(ApplicationUseCase, ICreateRequest):
    def __init__(
        self,
        event_publisher: IEventPublisher,
        request_repository: IRequestRepository,
    ):
        super().__init__(event_publisher)
        self._request_repository = request_repository

    async def __call__(self, command: CreateRequestCommand) -> Request:
        preferred_datetime = _build_request_datetime(
            command.preferred_date,
            command.preferred_time_start,
            command.preferred_time_end,
        )

        request = Request.create(
            user_id=command.requester,
            queue_id=command.queue_id,
            purpose=command.purpose,
            priority=RequestPriority.MEDIUM,
            preferred_datetime=preferred_datetime,
        )

        await self._request_repository.save(request)
        await self._publish_events(request)

        return request


def _build_request_datetime(
    preferred_date: date,
    preferred_time_start: time,
    preferred_time_end: time,
) -> RequestDateTime:
    time_period = TimePeriod(
        start_time=preferred_time_start,
        end_time=preferred_time_end,
    )
    return RequestDateTime(date=preferred_date, time_period=time_period)

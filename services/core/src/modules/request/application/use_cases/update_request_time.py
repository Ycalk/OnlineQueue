from datetime import datetime, timedelta

from ._base import RequestOwnerUseCase
from modules.request.domain.commands import (
    UpdateRequestTime as UpdateRequestTimeCommand,
)
from modules.request.domain.ports.inbound import IUpdateRequestTime
from modules.request.domain.value_objects import RequestDateTime, TimePeriod


class UpdateRequestTime(RequestOwnerUseCase, IUpdateRequestTime):
    async def __call__(self, command: UpdateRequestTimeCommand) -> None:
        request = await self._load_and_check_owner(
            command.request_id,
            command.requester,
        )

        confirmed_datetime = _build_confirmed_datetime(
            command.date,
            command.time_start,
            command.duration_minutes,
        )

        # Доменно: назначение конкретного слота = принятие заявки с этим временем
        request.accept(confirmed_datetime=confirmed_datetime)

        await self._request_repository.save(request)
        await self._publish_events(request)


def _build_confirmed_datetime(
    date_value,
    time_start,
    duration_minutes: int,
) -> RequestDateTime:
    start_dt = datetime.combine(date_value, time_start)
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    time_period = TimePeriod(
        start_time=start_dt.time(),
        end_time=end_dt.time(),
    )

    return RequestDateTime(date=date_value, time_period=time_period)

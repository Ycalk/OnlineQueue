from datetime import datetime

from modules.request.application.dto import (
    Request as RequestDto,
    ConfirmationHistoryItem,
    StatusHistoryItem,
)
from modules.request.domain.aggregates import Request as RequestAggregate
from modules.request.domain.value_objects import (
    RequestDateTime,
    RequestStatusHistoryItem,
    RequestConfirmationHistoryItem,
)


def _fmt_date(d: datetime) -> str:
    return d.date().isoformat()


def _fmt_time(d: datetime) -> str:
    return d.time().strftime("%H:%M")


def _from_request_datetime(dt: RequestDateTime | None):
    if dt is None:
        return None, None, None
    start = dt.start_period
    end = dt.end_period
    return (
        dt.date.isoformat(),
        start.strftime("%H:%M"),
        end.strftime("%H:%M"),
    )


def _map_status_history_item(item: RequestStatusHistoryItem) -> StatusHistoryItem:
    return StatusHistoryItem(
        status=item.status,
        updated_at=int(item.updated_at.timestamp()),
    )


def _map_confirmation_history_item(
    item: RequestConfirmationHistoryItem,
) -> ConfirmationHistoryItem:
    # updated_at уже есть как datetime
    return ConfirmationHistoryItem(
        date=item.date.isoformat(),
        time_start=item.time_start.strftime("%H:%M"),
        time_end=item.time_end.strftime("%H:%M"),
        updated_at=int(item.updated_at.timestamp()),
    )


def map_request(request: RequestAggregate) -> RequestDto:
    preferred_date, preferred_start, preferred_end = _from_request_datetime(
        request.preferred_datetime
    )

    confirmed_date, confirmed_start, confirmed_end = _from_request_datetime(
        request.confirmed_datetime
    )

    status_history = [
        _map_status_history_item(item) for item in request.status_history
    ]
    confirmation_history = [
        _map_confirmation_history_item(item)
        for item in request.confirmation_history
    ]

    return RequestDto(
        id=request.id.value,
        purpose=request.purpose,
        user_id=request.user_id.value,
        queue_id=request.queue_id.value,
        preferred_date=preferred_date,
        preferred_time_start=preferred_start,
        preferred_time_end=preferred_end,
        confirmed_date=confirmed_date,
        confirmed_time_start=confirmed_start,
        confirmed_time_end=confirmed_end,
        confirmation_history=confirmation_history,
        status_history=status_history,
        is_archived=request.archived,
        priority=request.priority,
        status=request.status,
        created_at=int(request.created_at.timestamp()),
        updated_at=int(request.updated_at.timestamp())
        if request.updated_at
        else None,
    )

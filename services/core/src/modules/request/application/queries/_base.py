from abc import ABC

from modules.request.application.ports.outbound.request_reader import IRequestReader
from modules.request.application.dto import (
    Request as RequestDTO,
    RequestDatetime as RequestDatetimeDTO,
    ConfirmationDatetimeHistoryItem as ConfirmationDatetimeHistoryItemDTO,
)
from modules.request.domain.aggregates import Request as RequestDomain
from modules.request.domain.value_objects import (
    RequestDatetime as RequestDatetimeDomain,
    RequestConfirmationDatetimeHistoryItem as RequestConfirmationDatetimeHistoryItemDomain,
)


class BaseRequestQuery(ABC):
    def __init__(self, request_reader: IRequestReader):
        self._request_reader = request_reader

    def _request_datetime_to_dto(
        self, request_datetime: RequestDatetimeDomain
    ) -> RequestDatetimeDTO:
        return RequestDatetimeDTO(
            date=request_datetime.date.isoformat(),
            time_start=request_datetime.time_period.start_time.isoformat(
                timespec="minutes"
            ),
            time_end=request_datetime.time_period.end_time.isoformat(
                timespec="minutes"
            ),
            start_unix=int(request_datetime.start_period.timestamp()),
            end_unix=int(request_datetime.end_period.timestamp()),
        )

    def _confirmation_datetime_history_item_to_dto(
        self, item: RequestConfirmationDatetimeHistoryItemDomain
    ) -> ConfirmationDatetimeHistoryItemDTO:
        request_datetime = self._request_datetime_to_dto(item.confirmation_datetime)
        return ConfirmationDatetimeHistoryItemDTO(
            date=request_datetime.date,
            time_start=request_datetime.time_start,
            time_end=request_datetime.time_end,
            start_unix=request_datetime.start_unix,
            end_unix=request_datetime.end_unix,
            occurred_at=int(item.occurred_at.timestamp()),
        )

    def _request_to_dto(self, aggregate: RequestDomain) -> RequestDTO:
        return RequestDTO(
            id=aggregate.id.value,
            purpose=aggregate.purpose.value,
            user_id=aggregate.user_id.value,
            queue_id=aggregate.queue.id.value,
            preferred_datetime=self._request_datetime_to_dto(
                aggregate.preferred_datetime
            ),
            confirmed_datetime=self._request_datetime_to_dto(
                aggregate.confirmed_datetime
            )
            if aggregate.confirmed_datetime
            else None,
            confirmation_datetime_history=[
                self._confirmation_datetime_history_item_to_dto(item)
                for item in aggregate.confirmation_datetime_history
            ],
            status_history=aggregate.status_history,
            priority_history=aggregate.priority_history,
            comments=aggregate.comments,
            is_archived=aggregate.archived,
            priority=aggregate.priority,
            status=aggregate.status,
        )

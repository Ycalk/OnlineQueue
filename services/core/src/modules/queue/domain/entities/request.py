from pydantic import BaseModel, model_validator
from datetime import datetime
from modules.queue.domain.value_objects import (
    RequestDateTime,
    RequestStatusHistoryItem,
    RequestStatus,
    UserId,
    RequestId,
)
from modules.queue.domain.errors import NotConsistentFields


def _get_request_status(
    status_history: list[RequestStatusHistoryItem],
) -> RequestStatus:
    return min(status_history, key=lambda x: x.updated_at).status


class Request(BaseModel):
    id: RequestId
    user_id: UserId
    preferred_time: RequestDateTime
    confirmed_time: RequestDateTime | None = None
    status_history: list[RequestStatusHistoryItem]
    archived: bool
    created_at: datetime

    @property
    def status(self) -> RequestStatus:
        return _get_request_status(self.status_history)

    def archive(self) -> None:
        self.archived = True

    def calculate_duration_seconds(self) -> int | None:
        if self.confirmed_time is None:
            return None
        return int(
            self.confirmed_time.end_period.timestamp()
            - self.confirmed_time.start_period.timestamp()
        )

    @model_validator(mode="after")
    def check_confirmed_time(cls, values):
        confirmed_time: RequestDateTime | None = values.get("confirmed_time")
        status_history: list[RequestStatusHistoryItem] = values.get("status_history")
        archived: bool = values.get("archived")
        current_status = _get_request_status(status_history)

        if current_status == RequestStatus.ACCEPTED and confirmed_time is None:
            raise NotConsistentFields(
                "Confirmed time is required when request is accepted"
            )
        elif current_status == RequestStatus.PENDING and confirmed_time is not None:
            raise NotConsistentFields(
                "Confirmed time must not be set when request is pending"
            )
        elif current_status == RequestStatus.REJECTED and not archived:
            raise NotConsistentFields("Request must be archived when rejected")
        return values

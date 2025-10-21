from pydantic import BaseModel
from .user import User
from modules.queue.domain.value_objects import SlotDuration

# TODO: добавить request id вместо uuid.UUID
# from modules.request.domain.aggregates import RequestId
from uuid import UUID


class Request(BaseModel):
    id: UUID
    user: User
    slot_duration: SlotDuration

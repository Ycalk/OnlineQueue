from uuid import UUID
from pydantic import BaseModel


class GetQueueRequests(BaseModel):
    queue_id: UUID

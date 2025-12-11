from uuid import UUID
from pydantic import BaseModel


class GetRequest(BaseModel):
    request_id: UUID
    requester_id: UUID

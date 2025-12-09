from uuid import UUID
from pydantic import BaseModel


class GetUserRequests(BaseModel):
    user_id: UUID

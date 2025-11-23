from pydantic import BaseModel


class GetQueueList(BaseModel):
    skip: int = 0
    limit: int | None = None

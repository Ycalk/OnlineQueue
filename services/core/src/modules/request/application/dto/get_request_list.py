from pydantic import BaseModel


class GetRequestList(BaseModel):
    skip: int = 0
    limit: int | None = None

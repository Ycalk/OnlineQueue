from pydantic import BaseModel, Field


class HTTPError(BaseModel):
    detail: str = Field(description="Детали ошибки")

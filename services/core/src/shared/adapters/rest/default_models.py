from pydantic import BaseModel, Field


class HTTPError(BaseModel):
    detail: str = Field(description="Детали ошибки")


class MessageResponse(BaseModel):
    message: str

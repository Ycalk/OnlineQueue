from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str = Field(description="Тип ошибки")
    message: str = Field(description="Детали ошибки")

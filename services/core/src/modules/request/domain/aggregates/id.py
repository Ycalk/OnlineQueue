from uuid import UUID, uuid4
from typing import Self

from pydantic import BaseModel, ConfigDict, Field


class RequestId(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: UUID = Field(default_factory=uuid4)

    @classmethod
    def from_uuid(cls, value: UUID) -> Self:
        return cls(value=value)

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(value=UUID(value))

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RequestId):
            return False
        return self.value == other.value

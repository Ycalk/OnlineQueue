from datetime import datetime
from abc import ABC
from pydantic import BaseModel, Field
from typing import ClassVar


class BaseEvent(BaseModel, ABC):
    name: ClassVar[str]
    occurred_at: datetime = Field(default_factory=datetime.now, init=False)

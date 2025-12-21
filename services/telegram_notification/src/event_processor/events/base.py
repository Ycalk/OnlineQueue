from datetime import datetime
from abc import ABC
from pydantic import BaseModel, Field
from typing import ClassVar


class BaseEvent(BaseModel, ABC):
    name: ClassVar[str]
    occurred_at: datetime = Field(default_factory=datetime.now, init=False)

    @classmethod
    def get_event_name(cls) -> str:
        """Получить имя события для exchange"""
        return cls.__dict__.get('name', cls.__name__)
from abc import ABC
from pydantic import BaseModel


class DomainEvent(ABC, BaseModel): ...

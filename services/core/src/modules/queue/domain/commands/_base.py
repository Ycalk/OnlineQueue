from pydantic import BaseModel
from modules.queue.domain.value_objects import UserId


class BaseCommand(BaseModel):
    requester: UserId

from pydantic import BaseModel

from modules.request.domain.value_objects import UserId


class BaseCommand(BaseModel):
    """
    Базовая команда с обязательным requester для проверки прав.
    """

    requester: UserId

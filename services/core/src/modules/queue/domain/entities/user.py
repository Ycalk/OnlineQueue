from pydantic import BaseModel
from modules.user.domain.aggregates import UserId


class User(BaseModel):
    id: UserId

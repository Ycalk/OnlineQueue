from pydantic import BaseModel
from modules.user.domain.aggregates import UserId


class ChangePassword(BaseModel):
    user_id: UserId
    old_password: str
    new_password: str

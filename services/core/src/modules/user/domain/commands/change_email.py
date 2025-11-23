from pydantic import BaseModel
from modules.user.domain.aggregates import UserId
from modules.user.domain.value_objects import Email


class ChangeEmail(BaseModel):
    user_id: UserId
    new_email: Email
    password: str

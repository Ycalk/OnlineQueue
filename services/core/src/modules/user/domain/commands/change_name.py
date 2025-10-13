from pydantic import BaseModel
from modules.user.domain.aggregates import UserId


class ChangeName(BaseModel):
    user_id: UserId
    new_first_name: str | None = None
    new_last_name: str | None = None
    new_patronymic: str | None = None

from pydantic import BaseModel
from modules.user.domain.value_objects import Email, Name


class CreateUser(BaseModel):
    email: Email
    name: Name
    password: str

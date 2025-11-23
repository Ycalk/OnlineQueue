from pydantic import BaseModel
from modules.user.domain.value_objects import Email


class Login(BaseModel):
    email: Email
    plain_password: str

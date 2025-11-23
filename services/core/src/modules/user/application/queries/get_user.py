from uuid import UUID

from modules.user.application.ports.inbound.queries import IGetUser
from modules.user.application.ports.outbound.user_reader import IUserReader
from modules.user.application.dto import User
from modules.user.application.errors import UserNotFoundError


class GetUser(IGetUser):
    def __init__(self, user_reader: IUserReader):
        self._user_reader = user_reader

    async def __call__(self, user_id: UUID) -> User:
        user = await self._user_reader.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

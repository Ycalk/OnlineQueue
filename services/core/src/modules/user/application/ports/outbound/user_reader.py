from typing import Protocol
from uuid import UUID

from modules.user.application.dto import User


class IUserReader(Protocol):
    async def find_by_id(self, user_id: UUID) -> User | None:
        """Получение пользователя по id

        Args:
            user_id (UUID): id пользователя

        Returns:
            User | None: пользователь
        """

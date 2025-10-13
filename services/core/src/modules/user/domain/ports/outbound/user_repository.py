from typing import Protocol
from modules.user.domain.aggregates import User, UserId
from modules.user.domain.value_objects import Email


class IUserRepository(Protocol):
    async def save(self, user: User) -> None:
        """Сохранение или обновление пользователя

        Args:
            user (User): пользователь
        Raises:
            modules.user.application.errors.UserAlreadyExistsError: Если при обновление email нарушается уникальность
        """
        ...

    async def delete(self, user: User | UserId) -> None:
        """Удаление пользователя

        Args:
            user (User | UserId): агрегат или id
        """
        ...

    async def exists_by_id(self, user_id: UserId) -> bool:
        """Проверяет существование по id

        Args:
            user_id (UserId): id пользователя

        Returns:
            bool: True если пользователь существует
        """
        ...

    async def exists_by_email(self, email: Email) -> bool:
        """Проверяет существование по email

        Args:
            user_id (Email): email пользователя

        Returns:
            bool: True если пользователь существует
        """
        ...

    async def find_by_id(self, user_id: UserId) -> User | None:
        """Поиск пользователя по id

        Args:
            user_id (UserId): id пользователя

        Returns:
            User | None: пользователь
        """
        ...

    async def find_by_email(self, email: Email) -> User | None:
        """Поиск пользователя по email

        Args:
            email (Email): email пользователя

        Returns:
            User | None: пользователь
        """
        ...

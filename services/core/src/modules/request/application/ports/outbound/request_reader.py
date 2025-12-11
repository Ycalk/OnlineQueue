from typing import Protocol
from uuid import UUID

from modules.request.domain.aggregates import Request
from modules.request.domain.entities import Queue


class IRequestReader(Protocol):
    async def find_by_id(self, request_id: UUID) -> Request | None:
        """
        Поиск заявки по идентификатору.

        Args:
            request_id (UUID): идентификатор заявки.

        Returns:
            Request | None: найденная заявка или None.
        """
        ...

    async def find_queue_by_id(self, queue_id: UUID) -> Queue | None:
        """
        Поиск очереди по идентификатору.

        Args:
            queue_id (UUID): идентификатор очереди.

        Returns:
            Queue | None: найденная очередь или None.
        """
        ...

    async def get_by_user_id(
        self, user_id: UUID, skip: int, limit: int | None
    ) -> list[Request]:
        """
        Получение всех заявок конкретного пользователя.

        Args:
            user_id (UUID): идентификатор пользователя.

        Returns:
            list[Request]: список заявок конкретного пользователя.
        """
        ...

    async def get_by_queue_owner_id(self, owner_id: UUID) -> list[Request]:
        """
        Получение всех заявок из очередей в которых пользователь владелец.

        Args:
            owner_id (UUID): идентификатор владельца очереди.

        Returns:
            list[Request]: список заявок из очередей в которых пользователь владелец.
        """
        ...

    async def get_by_queue_id(self, queue_id: UUID) -> list[Request]:
        """
        Получение всех заявок в конкретной очереди.

        Args:
            queue_id (UUID): идентификатор очереди.

        Returns:
            list[Request]: список заявок в конкретной очереди.
        """
        ...

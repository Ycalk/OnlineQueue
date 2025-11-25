from typing import Protocol
from uuid import UUID

from modules.request.domain.aggregates import Request


class IRequestReader(Protocol):
    async def find_by_id(self, request_id: UUID) -> Request | None:
        """Получение заявки по id."""
        ...

    async def get_many(self, skip: int, limit: int | None) -> list[Request]:
        """Получение списка заявок (с пагинацией)."""
        ...

    async def find_by_user_id(self, user_id: UUID) -> list[Request]:
        """Получение всех заявок пользователя."""
        ...

    async def find_by_queue_id(self, queue_id: UUID) -> list[Request]:
        """Получение всех заявок в очереди (queue_id из bounded context request)."""
        ...

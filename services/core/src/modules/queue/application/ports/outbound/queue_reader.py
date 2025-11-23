from typing import Protocol
from uuid import UUID

from modules.queue.domain.aggregates.model import Queue


class IQueueReader(Protocol):
    async def find_by_id(self, queue_id: UUID) -> Queue | None:
        """Получение очереди по id

        Args:
            queue_id (UUID): id очереди

        Returns:
            Queue | None: очередь
        """
        ...

    async def get_many(self, skip: int, limit: int | None) -> list[Queue]:
        """Получение списка очередей

        Args:
            skip (int): смещение
            limit (int): лимит

        Returns:
            list[Queue]: список очередей
        """
        ...

    async def find_by_owner_id(self, owner_id: UUID) -> list[Queue]:
        """Получение списка очередей по id владельца

        Args:
            owner_id (UUID): id владельца

        Returns:
            list[Queue]: список очередей
        """
        ...

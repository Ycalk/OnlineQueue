from typing import Protocol

from modules.queue.domain.aggregates import Queue, QueueId
from modules.queue.domain.value_objects import RequestId


class IQueueRepository(Protocol):
    async def save(self, queue: Queue) -> None:
        """Сохранение или обновление очереди

        Args:
            queue (Queue): очередь
        """
        ...

    async def delete(self, queue: Queue | QueueId) -> None:
        """Удаление очереди

        Args:
            queue (Queue): очередь
        """
        ...

    async def exists(self, queue_id: QueueId) -> bool:
        """Проверка существования очереди

        Args:
            queue_id (QueueId): идентификатор очереди

        Returns:
            bool: True если очередь существует
        """
        ...

    async def find(self, queue_id: QueueId) -> Queue | None:
        """Поиск очереди по идентификатору

        Args:
            queue_id (QueueId): идентификатор очереди

        Returns:
            Queue | None: очередь
        """
        ...

    async def find_by_request_id(self, request_id: RequestId) -> Queue | None:
        """Поиск очереди по идентификатору запроса

        Args:
            request_id (RequestId): идентификатор запроса

        Returns:
            Queue | None: очередь
        """
        ...

    async def get_all(self) -> list[Queue]:
        """Получение всех очередей

        Returns:
            list[Queue]: список очередей
        """
        ...

    async def commit(self) -> None: ...

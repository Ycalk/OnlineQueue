from typing import Protocol
from modules.queue.domain.aggregates import Queue, QueueId


class IQueueRepository(Protocol):
    async def save(self, queue: Queue) -> None:
        """Сохранение или обновление пользователя

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

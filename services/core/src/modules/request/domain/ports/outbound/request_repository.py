from typing import Protocol

from modules.request.domain.aggregates import Request, RequestId
from modules.request.domain.value_objects import QueueId
from modules.request.domain.entities import Queue


class IRequestRepository(Protocol):
    async def save(self, request: Request) -> None:
        """Сохранение или обновление заявки.

        Args:
            request (Request): агрегат заявки.
        """
        ...

    async def exists(self, request_id: RequestId) -> bool:
        """Проверка существования заявки.

        Args:
            request_id (RequestId): идентификатор заявки.

        Returns:
            bool: True если заявка существует.
        """
        ...

    async def find_by_id(self, request_id: RequestId) -> Request | None:
        """Поиск заявки по идентификатору.

        Args:
            request_id (RequestId): идентификатор заявки.

        Returns:
            Request | None: найденная заявка или None.
        """
        ...

    async def find_queue_by_id(self, queue_id: QueueId) -> Queue | None:
        """Поиск очереди по идентификатору.

        Args:
            queue_id (QueueId): идентификатор очереди.

        Returns:
            Queue | None: найденная очередь или None.
        """
        ...

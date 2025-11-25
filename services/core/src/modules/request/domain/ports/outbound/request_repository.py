from typing import Protocol

from modules.request.domain.aggregates import Request
from modules.request.domain.value_objects import RequestId, UserId, QueueId


class IRequestRepository(Protocol):
    async def save(self, request: Request) -> None:
        """Сохранение или обновление заявки.

        Args:
            request (Request): агрегат заявки.
        """
        ...

    async def delete(self, request: Request | RequestId) -> None:
        """Удаление заявки.

        Args:
            request (Request | RequestId): заявка или её идентификатор.
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

    async def find(self, request_id: RequestId) -> Request | None:
        """Поиск заявки по идентификатору.

        Args:
            request_id (RequestId): идентификатор заявки.

        Returns:
            Request | None: найденная заявка или None.
        """
        ...

    async def find_by_user_and_queue(
        self,
        user_id: UserId,
        queue_id: QueueId,
    ) -> list[Request]:
        """Поиск заявок пользователя в конкретной очереди.

        Это удобно для сценариев «мои записи в этой очереди».

        Args:
            user_id (UserId): идентификатор пользователя.
            queue_id (QueueId): идентификатор очереди.

        Returns:
            list[Request]: список заявок.
        """
        ...

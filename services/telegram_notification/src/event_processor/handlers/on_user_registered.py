from logging import getLogger

from .base import BaseEventHandler
from event_processor.events import UserRegistered


class OnUserRegistered(BaseEventHandler[UserRegistered]):
    @classmethod
    def event_type(cls) -> type[UserRegistered]:
        return UserRegistered

    def __init__(self):
        # Сюда можно еще передавать, например, сессию sqlAlchemy или инстанс бота
        self._logger = getLogger("event_handler.on_user_registered")

    async def __call__(self, event: UserRegistered) -> None:
        self._logger.info(
            (
                f"Registered user {event.user_id}. "
                f"Email: {event.email}, "
                f"First name: {event.first_name}, "
                f"Last name: {event.last_name}, "
                f"Patronymic: {event.patronymic}"
            )
        )

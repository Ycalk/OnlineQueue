from logging import getLogger
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import TelegramUser
from .base import BaseEventHandler
from event_processor.events import UserRegistered


class OnUserRegistered(BaseEventHandler[UserRegistered]):
    @classmethod
    def event_type(cls) -> type[UserRegistered]:
        return UserRegistered

    def __init__(self, session: AsyncSession):
        self._session = session
        self._logger = getLogger("event_handler.on_user_registered")

    async def __call__(self, event: UserRegistered) -> None:
        self._logger.info(
            f"Processing UserRegistered: user_id={event.user_id}, email={event.email}"
        )

        result = await self._session.execute(
            select(TelegramUser).where(TelegramUser.user_id == event.user_id)
        )
        user = result.scalar_one_or_none()

        if user:
            user.email = event.email
            user.first_name = event.first_name
            user.last_name = event.last_name
            user.patronymic = event.patronymic
            self._logger.info(f"Updated existing user {event.user_id}")
        else:
            new_user = TelegramUser(
                user_id=event.user_id,
                telegram_id=0,
                email=event.email,
                first_name=event.first_name,
                last_name=event.last_name,
                patronymic=event.patronymic,
            )
            self._session.add(new_user)
            self._logger.info(f"Created user record for {event.user_id}")

        await self._session.commit()

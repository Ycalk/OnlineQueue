from uuid import UUID
from modules.user.application.ports.outbound.user_reader import IUserReader

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.user.application.dto import User
from .models import User as UserSchema


class UserReader(IUserReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(
            select(UserSchema).where(UserSchema.id == user_id)
        )
        user_model = result.scalar_one_or_none()

        if user_model is not None:
            return User(
                email=user_model.email,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                patronymic=user_model.patronymic,
            )

        return None

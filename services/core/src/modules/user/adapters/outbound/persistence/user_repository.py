from typing import cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from sqlalchemy.exc import IntegrityError
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.domain.aggregates import User, UserId
from modules.user.domain.value_objects import Email, Name, HashedPassword
from modules.user.application.errors import UserAlreadyExistsError
from shared.persistence import User as UserSchema


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> None:
        user_model = self._to_orm(user)

        try:
            self._session.add(user_model)
            await self._session.flush()
        except IntegrityError as e:
            if "unique" in str(e).lower() and "email" in str(e).lower():
                raise UserAlreadyExistsError(
                    f"User with email {user.email} already exists"
                ) from e
            raise

    async def delete(self, user: User | UserId) -> None:
        if isinstance(user, User):
            user_id = user.id.value
        else:
            user_id = user.value

        await self._session.execute(delete(UserSchema).where(UserSchema.id == user_id))

    async def exists_by_id(self, user_id: UserId) -> bool:
        result = await self._session.execute(
            select(exists().where(UserSchema.id == user_id.value))
        )
        return cast(bool, result.scalar())

    async def exists_by_email(self, email: Email) -> bool:
        result = await self._session.execute(
            select(exists().where(UserSchema.email == email.value))
        )
        return cast(bool, result.scalar())

    async def find_by_id(self, user_id: UserId) -> User | None:
        result = await self._session.execute(
            select(UserSchema).where(UserSchema.id == user_id.value)
        )
        user_model = result.scalar_one_or_none()

        if user_model is not None:
            return self._to_domain(user_model)

    async def find_by_email(self, email: Email) -> User | None:
        result = await self._session.execute(
            select(UserSchema).where(UserSchema.email == email.value)
        )
        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return self._to_domain(user_model)

    def _to_orm(self, user: User) -> UserSchema:
        return UserSchema(
            id=user.id.value,
            email=user.email.value,
            first_name=user.name.first_name,
            last_name=user.name.last_name,
            patronymic=user.name.patronymic,
            password_hash=user.hashed_password.value,
        )

    def _to_domain(self, model: UserSchema) -> User:
        return User(
            id=UserId.from_uuid(model.id),
            email=Email(value=model.email),
            name=Name(
                first_name=model.first_name,
                last_name=model.last_name,
                patronymic=model.patronymic,
            ),
            hashed_password=HashedPassword(value=model.password_hash),
        )

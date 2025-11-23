import pytest
from modules.user.domain.aggregates import User, UserId
from modules.user.domain.value_objects import Email, Name, HashedPassword
from modules.user.adapters.outbound.persistence.user_repository import UserRepository
from modules.user.domain.ports.outbound import IUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="function")
def user_password() -> str:
    return "StrongPassword123"


@pytest.fixture(scope="function")
def user_id() -> UserId:
    return UserId()


@pytest.fixture(scope="function")
def email() -> Email:
    return Email(value="user@example.com")


@pytest.fixture(
    scope="function",
    params=[
        {"first_name": "John", "last_name": "Doe", "patronymic": None},
        {"first_name": "Иван", "last_name": "Петров", "patronymic": "Сергеевич"},
    ],
    ids=["without_patronymic", "with_patronymic"],
)
def name(request) -> Name:
    return Name(**request.param)


@pytest.fixture(scope="function")
def hashed_password(user_password: str) -> HashedPassword:
    return HashedPassword.from_plain_password(user_password)


@pytest.fixture(scope="function")
def user(
    user_id: UserId, email: Email, name: Name, hashed_password: HashedPassword
) -> User:
    return User(id=user_id, email=email, name=name, hashed_password=hashed_password)


@pytest.fixture(scope="function")
def user_repository(session: AsyncSession) -> IUserRepository:
    return UserRepository(session)

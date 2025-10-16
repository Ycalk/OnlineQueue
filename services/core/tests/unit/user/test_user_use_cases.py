import pytest
import pytest_asyncio
from modules.user.application.use_cases import (
    CreateUser,
    Login,
    ChangePassword,
    ChangeName,
    ChangeEmail,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tests.conftest import EventPublisherCounter
from shared.persistence.models import User as UserSchema
from modules.user.application.errors import UserNotFoundError, UserAlreadyExistsError
from modules.user.domain.aggregates import User, UserId
from modules.user.domain.value_objects import Email, Name, HashedPassword
from modules.user.domain.errors import (
    InvalidPasswordError,
    WeakPasswordError,
    SamePasswordError,
    SameEmailError,
)
from modules.user.domain.events import (
    UserRegistered,
    UserLogin,
    PasswordChanged,
    EmailChanged,
    NameChanged,
)
from modules.user.domain.ports.outbound import IUserRepository
from modules.user.domain.commands import CreateUser as CreateUserCommand
from modules.user.domain.commands import Login as LoginCommand
from modules.user.domain.commands import ChangePassword as ChangePasswordCommand
from modules.user.domain.commands import ChangeName as ChangeNameCommand
from modules.user.domain.commands import ChangeEmail as ChangeEmailCommand


@pytest_asyncio.fixture(scope="function")
async def existing_user(
    session: AsyncSession,
    email: Email,
    name: Name,
    user_password: str,
) -> User:
    user = User.register(email=email, name=name, plain_password=user_password)
    session.add(
        UserSchema(
            email=user.email.value,
            first_name=user.name.first_name,
            last_name=user.name.last_name,
            patronymic=user.name.patronymic,
            password_hash=user.hashed_password.value,
            id=user.id.value,
        )
    )
    await session.commit()
    return user


@pytest.fixture(scope="function")
def create_user_use_case(
    event_publisher: EventPublisherCounter,
    user_repository: IUserRepository,
) -> CreateUser:
    return CreateUser(event_publisher, user_repository)


@pytest.fixture(scope="function")
def login_use_case(
    event_publisher: EventPublisherCounter,
    user_repository: IUserRepository,
) -> Login:
    return Login(event_publisher, user_repository)


@pytest.fixture(scope="function")
def change_password_use_case(
    event_publisher: EventPublisherCounter,
    user_repository: IUserRepository,
) -> ChangePassword:
    return ChangePassword(event_publisher, user_repository)


@pytest.fixture(scope="function")
def change_email_use_case(
    event_publisher: EventPublisherCounter,
    user_repository: IUserRepository,
) -> ChangeEmail:
    return ChangeEmail(event_publisher, user_repository)


@pytest.fixture(scope="function")
def change_name_use_case(
    event_publisher: EventPublisherCounter,
    user_repository: IUserRepository,
) -> ChangeName:
    return ChangeName(event_publisher, user_repository)


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_user_successfully(
        self,
        session: AsyncSession,
        create_user_use_case: CreateUser,
        email: Email,
        name: Name,
        user_password: str,
    ):
        """Успешное создание пользователя."""
        user = await create_user_use_case(
            CreateUserCommand(email=email, name=name, password=user_password)
        )

        result = await session.scalar(select(UserSchema))

        assert result is not None
        assert email.value == result.email
        assert name.first_name == result.first_name
        assert name.last_name == result.last_name
        assert name.patronymic == result.patronymic

        assert user.hashed_password.verify(user_password)

    @pytest.mark.asyncio
    async def test_create_user_with_existing_email(
        self,
        create_user_use_case: CreateUser,
        existing_user: User,
        user_password: str,
    ):
        """Создание пользователя с существующим email."""
        with pytest.raises(UserAlreadyExistsError):
            await create_user_use_case(
                CreateUserCommand(
                    email=existing_user.email,
                    name=existing_user.name,
                    password=user_password,
                )
            )

    @pytest.mark.asyncio
    async def test_create_user_with_weak_password(
        self,
        create_user_use_case: CreateUser,
        email: Email,
        name: Name,
    ):
        """Создание пользователя с слабым паролем."""
        with pytest.raises(WeakPasswordError):
            await create_user_use_case(
                CreateUserCommand(email=email, name=name, password="weak")
            )

    @pytest.mark.asyncio
    async def test_create_user_publishes_event(
        self,
        event_publisher: EventPublisherCounter,
        user_repository: IUserRepository,
        email: Email,
        name: Name,
        user_password: str,
    ):
        """Создание пользователя публикует событие."""
        use_case = CreateUser(event_publisher, user_repository)
        await use_case(
            CreateUserCommand(email=email, name=name, password=user_password)
        )

        event = event_publisher.events[0]

        assert isinstance(event, UserRegistered)
        assert event.email.value == email.value
        assert event.name.first_name == name.first_name
        assert event.name.last_name == name.last_name
        assert event.name.patronymic == name.patronymic


class TestLogin:
    @pytest.mark.asyncio
    async def test_login_successfully(
        self,
        login_use_case: Login,
        existing_user: User,
        user_password: str,
    ):
        """Успешный вход."""
        user = await login_use_case(
            LoginCommand(email=existing_user.email, plain_password=user_password)
        )

        assert user.id == existing_user.id
        assert user.name == existing_user.name
        assert user.email == existing_user.email
        assert user.hashed_password.verify(user_password)

    @pytest.mark.asyncio
    async def test_login_with_nonexistent_user(
        self, login_use_case: Login, email: Email
    ):
        """Вход с несуществующим пользователем."""
        with pytest.raises(UserNotFoundError):
            await login_use_case(
                LoginCommand(email=email, plain_password="Password123")
            )

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(
        self, login_use_case: Login, existing_user: User
    ):
        """Вход с неправильным паролем."""
        with pytest.raises(InvalidPasswordError):
            await login_use_case(
                LoginCommand(
                    email=existing_user.email,
                    plain_password=existing_user.hashed_password.value,
                )
            )

    @pytest.mark.asyncio
    async def test_login_publishes_event(
        self,
        event_publisher: EventPublisherCounter,
        user_repository: IUserRepository,
        existing_user: User,
        user_password: str,
    ):
        """Вход публикует событие."""
        use_case = Login(event_publisher, user_repository)
        await use_case(
            LoginCommand(email=existing_user.email, plain_password=user_password)
        )

        event = event_publisher.events[0]

        assert isinstance(event, UserLogin)
        assert event.user_id == existing_user.id
        assert event.email == existing_user.email


class TestChangePassword:
    @pytest.mark.asyncio
    async def test_change_password_successfully(
        self,
        change_password_use_case: ChangePassword,
        user_password: str,
        existing_user: User,
        session: AsyncSession,
    ):
        """Успешная смена пароля."""
        new_pass = "NewPassword456"
        await change_password_use_case(
            ChangePasswordCommand(
                user_id=existing_user.id,
                old_password=user_password,
                new_password=new_pass,
            )
        )

        updated_user = await session.scalar(
            select(UserSchema).where(UserSchema.id == existing_user.id.value)
        )

        assert updated_user is not None
        assert HashedPassword.verify(
            HashedPassword(value=updated_user.password_hash), new_pass
        )

        assert updated_user.email == existing_user.email.value
        assert updated_user.first_name == existing_user.name.first_name
        assert updated_user.last_name == existing_user.name.last_name
        assert updated_user.patronymic == existing_user.name.patronymic

    @pytest.mark.asyncio
    async def test_change_password_for_nonexistent_user(
        self, change_password_use_case: ChangePassword, user: User, user_password: str
    ):
        """Смена пароля для несуществующего пользователя."""
        with pytest.raises(UserNotFoundError):
            await change_password_use_case(
                ChangePasswordCommand(
                    user_id=user.id,
                    old_password=user_password,
                    new_password="NewPassword456",
                )
            )

    @pytest.mark.asyncio
    async def test_change_password_with_wrong_old_password(
        self, change_password_use_case: ChangePassword, existing_user: User
    ):
        """Смена пароля с неправильным старым паролем."""
        with pytest.raises(InvalidPasswordError):
            await change_password_use_case(
                ChangePasswordCommand(
                    user_id=existing_user.id,
                    old_password="WrongPassword123",
                    new_password="NewPassword456",
                )
            )

    @pytest.mark.asyncio
    async def test_change_password_to_same_password(
        self,
        change_password_use_case: ChangePassword,
        existing_user: User,
        user_password: str,
    ):
        """Смена пароля на то же самое."""
        with pytest.raises(SamePasswordError):
            await change_password_use_case(
                ChangePasswordCommand(
                    user_id=existing_user.id,
                    old_password=user_password,
                    new_password=user_password,
                )
            )

    @pytest.mark.asyncio
    async def test_change_password_to_weak_password(
        self,
        change_password_use_case: ChangePassword,
        existing_user: User,
        user_password: str,
    ):
        """Смена пароля на слабый."""
        with pytest.raises(WeakPasswordError):
            await change_password_use_case(
                ChangePasswordCommand(
                    user_id=existing_user.id,
                    old_password=user_password,
                    new_password="weak",
                )
            )

    @pytest.mark.asyncio
    async def test_change_password_publishes_event(
        self,
        event_publisher: EventPublisherCounter,
        user_repository: IUserRepository,
        existing_user: User,
        user_password: str,
    ):
        """Смена пароля публикует событие."""
        use_case = ChangePassword(event_publisher, user_repository)
        await use_case(
            ChangePasswordCommand(
                user_id=existing_user.id,
                old_password=user_password,
                new_password="NewPassword456",
            )
        )

        event = event_publisher.events[0]

        assert isinstance(event, PasswordChanged)
        assert event.user_id == existing_user.id
        assert event.email == existing_user.email


class TestChangeName:
    @pytest.mark.asyncio
    async def test_change_name_successfully(
        self,
        change_name_use_case: ChangeName,
        existing_user: User,
        session: AsyncSession,
    ):
        """Успешная смена имени."""
        new_name = Name(first_name="Иван", last_name="Петров", patronymic="Сергеевич")

        await change_name_use_case(
            ChangeNameCommand(
                user_id=existing_user.id,
                new_first_name=new_name.first_name,
                new_last_name=new_name.last_name,
                new_patronymic=new_name.patronymic,
            )
        )

        updated_user = await session.scalar(
            select(UserSchema).where(UserSchema.id == existing_user.id.value)
        )

        assert updated_user is not None
        assert updated_user.first_name == new_name.first_name
        assert updated_user.last_name == new_name.last_name
        assert updated_user.patronymic == new_name.patronymic

    @pytest.mark.asyncio
    async def test_change_name_for_nonexistent_user(
        self, change_name_use_case: ChangeName, name: Name, user: User
    ):
        """Смена имени для несуществующего пользователя."""
        with pytest.raises(UserNotFoundError):
            await change_name_use_case(
                ChangeNameCommand(
                    user_id=user.id,
                    new_first_name=name.first_name,
                    new_last_name=name.last_name,
                    new_patronymic=name.patronymic,
                )
            )

    @pytest.mark.asyncio
    async def test_change_name_publishes_event(
        self,
        event_publisher: EventPublisherCounter,
        user_repository: IUserRepository,
        existing_user: User,
    ):
        """Смена имени публикует событие."""
        use_case = ChangeName(event_publisher, user_repository)
        await use_case(
            ChangeNameCommand(
                user_id=existing_user.id,
                new_first_name="Иван",
                new_last_name="Петров",
                new_patronymic="Сергеевич",
            )
        )

        event = event_publisher.events[0]

        assert isinstance(event, NameChanged)
        assert event.user_id == existing_user.id
        assert event.email == existing_user.email


class TestChangeEmail:
    @pytest.mark.asyncio
    async def test_change_email_successfully(
        self,
        change_email_use_case: ChangeEmail,
        existing_user: User,
        user_password: str,
        session: AsyncSession,
    ):
        """Успешная смена email."""
        new_email = Email(value="newemail@example.com")

        await change_email_use_case(
            ChangeEmailCommand(
                user_id=existing_user.id,
                new_email=new_email,
                password=user_password,
            )
        )

        updated_user = await session.scalar(
            select(UserSchema).where(UserSchema.id == existing_user.id.value)
        )

        assert updated_user is not None
        assert updated_user.email == new_email.value

    @pytest.mark.asyncio
    async def test_change_email_for_nonexistent_user(
        self,
        change_email_use_case: ChangeEmail,
        user_password: str,
    ):
        """Смена email для несуществующего пользователя."""
        non_existent_id = UserId()
        new_email = Email(value="new@example.com")

        with pytest.raises(UserNotFoundError):
            await change_email_use_case(
                ChangeEmailCommand(
                    user_id=non_existent_id,
                    new_email=new_email,
                    password=user_password,
                )
            )

    @pytest.mark.asyncio
    async def test_change_email_to_existing_email(
        self,
        change_email_use_case: ChangeEmail,
        existing_user: User,
        user_password: str,
        session: AsyncSession,
    ):
        """Смена email на уже существующий."""
        another_user = User.register(
            email=Email(value="another@example.com"),
            name=Name(first_name="Другой", last_name="Пользователь", patronymic=None),
            plain_password=user_password,
        )
        session.add(
            UserSchema(
                email=another_user.email.value,
                first_name=another_user.name.first_name,
                last_name=another_user.name.last_name,
                patronymic=another_user.name.patronymic,
                password_hash=another_user.hashed_password.value,
                id=another_user.id.value,
            )
        )
        await session.commit()

        with pytest.raises(UserAlreadyExistsError):
            await change_email_use_case(
                ChangeEmailCommand(
                    user_id=existing_user.id,
                    new_email=Email(value="another@example.com"),
                    password=user_password,
                )
            )

    @pytest.mark.asyncio
    async def test_change_email_with_wrong_password(
        self,
        change_email_use_case: ChangeEmail,
        existing_user: User,
    ):
        """Смена email с неправильным паролем."""
        new_email = Email(value="newemail@example.com")

        with pytest.raises(InvalidPasswordError):
            await change_email_use_case(
                ChangeEmailCommand(
                    user_id=existing_user.id,
                    new_email=new_email,
                    password="WrongPassword123",
                )
            )

    @pytest.mark.asyncio
    async def change_email_to_same_email(
        self,
        change_email_use_case: ChangeEmail,
        existing_user: User,
        user_password: str,
    ):
        """Смена email на такой же email."""
        with pytest.raises(SameEmailError):
            await change_email_use_case(
                ChangeEmailCommand(
                    user_id=existing_user.id,
                    new_email=existing_user.email,
                    password=user_password,
                )
            )

    @pytest.mark.asyncio
    async def test_change_email_publishes_event(
        self,
        event_publisher: EventPublisherCounter,
        user_repository: IUserRepository,
        existing_user: User,
        user_password: str,
    ):
        """Смена email публикует событие."""
        use_case = ChangeEmail(event_publisher, user_repository)
        await use_case(
            ChangeEmailCommand(
                user_id=existing_user.id,
                new_email=Email(value="newemail@example.com"),
                password=user_password,
            )
        )

        event = event_publisher.events[0]

        assert isinstance(event, EmailChanged)
        assert event.user_id == existing_user.id
        assert event.old_email == existing_user.email
        assert event.new_email == Email(value="newemail@example.com")

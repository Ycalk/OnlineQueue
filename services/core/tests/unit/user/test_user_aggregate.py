import pytest
from modules.user.domain.aggregates import User, UserId
from modules.user.domain.value_objects import Email, Name, HashedPassword
from modules.user.domain.events import (
    UserRegistered,
    UserLogin,
    PasswordChanged,
    EmailChanged,
    NameChanged,
)
from modules.user.domain.errors import (
    InvalidPasswordError,
    SamePasswordError,
    SameEmailError,
)


class TestUserCreation:
    def test_create_user(
        self, user_id: UserId, email: Email, name: Name, hashed_password: HashedPassword
    ):
        """Успешное создание пользователя."""
        user = User(id=user_id, email=email, name=name, hashed_password=hashed_password)

        assert user.id == user_id
        assert user.email == email
        assert user.name == name
        assert user.hashed_password == hashed_password
        assert len(user.events) == 0

    def test_register_user(self, email: Email, name: Name, user_password: str):
        """Регистрация нового пользователя."""
        user = User.register(email=email, name=name, plain_password=user_password)

        assert user.email == email
        assert user.name == name
        assert user.hashed_password.verify(user_password)
        assert len(user.events) == 1
        assert isinstance(user.events[0], UserRegistered)


class TestUserLogin:
    def test_login_with_correct_password(self, user: User, user_password: str):
        """Успешный вход с правильным паролем."""
        user.login(user_password)

        assert len(user.events) == 1
        assert isinstance(user.events[0], UserLogin)

    def test_login_with_incorrect_password_raises_error(self, user: User):
        """Вход с неправильным паролем вызывает ошибку."""
        with pytest.raises(InvalidPasswordError):
            user.login("WrongPassword")


class TestPasswordChange:
    def test_change_password_successfully(self, user: User, user_password: str):
        """Успешная смена пароля."""
        old_password = user_password
        new_password = "NewStrongPassword456"

        user.change_password(old_password, new_password)

        assert user.hashed_password.verify(new_password)
        assert not user.hashed_password.verify(old_password)
        assert len(user.events) == 1
        assert isinstance(user.events[0], PasswordChanged)

    def test_change_password_with_wrong_old_password(self, user: User):
        """Смена пароля с неправильным старым паролем."""
        with pytest.raises(InvalidPasswordError):
            user.change_password("WrongPassword", "NewPassword123")

    def test_change_password_to_same_password(self, user: User, user_password: str):
        """Смена пароля на такой же пароль."""
        with pytest.raises(SamePasswordError):
            user.change_password(user_password, user_password)


class TestEmailChange:
    def test_change_email_successfully(self, user: User, user_password: str):
        """Успешная смена email."""
        new_email = Email(value="newemail@example.com")

        user.change_email(new_email, user_password)

        assert user.email == new_email
        assert len(user.events) == 1
        assert isinstance(user.events[0], EmailChanged)

    def test_change_email_with_wrong_password(self, user: User):
        """Смена email с неправильным паролем."""
        new_email = Email(value="newemail@example.com")

        with pytest.raises(InvalidPasswordError):
            user.change_email(new_email, "WrongPassword")

    def test_change_email_to_same_email(self, user: User, user_password: str):
        """Смена email на такой же email."""
        with pytest.raises(SameEmailError):
            user.change_email(user.email, user_password)


class TestNameChange:
    def test_change_name_successfully(self, user: User, name: Name):
        """Успешная смена имени."""
        user.change_name(name)

        assert user.name == name
        assert len(user.events) == 1
        assert isinstance(user.events[0], NameChanged)

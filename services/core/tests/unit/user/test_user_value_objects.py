import pytest
from modules.user.domain.value_objects import Email, Name, HashedPassword
from modules.user.domain.errors import WeakPasswordError
from pydantic import ValidationError


class TestEmail:
    def test_create_valid_email(self):
        """Успешное создание валидного email."""
        email = Email(value="user@example.com")
        assert email.value == "user@example.com"

    def test_create_invalid_email_raises_error(self):
        """Создание невалидного email вызывает ошибку."""
        with pytest.raises(ValidationError):
            Email(value="invalid-email")

    def test_email_is_normalized(self):
        """Email приводится к нижнему регистру."""
        email = Email(value="User@Example.COM")
        assert email.value == "user@example.com"

    def test_email_equality(self):
        """Два email с одинаковым значением равны."""
        email1 = Email(value="test@example.com")
        email2 = Email(value="test@example.com")
        assert email1 == email2

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "",
            "notanemail",
            "@example.com",
            "user@",
            "user @example.com",
            "user@.com",
        ],
    )
    def test_invalid_email_formats(self, invalid_email):
        """Различные невалидные форматы email."""
        with pytest.raises(ValidationError):
            Email(value=invalid_email)


class TestName:
    def test_create_valid_name(self):
        """Успешное создание валидного имени."""
        name = Name(first_name="John", last_name="Doe")
        assert name.first_name == "John"
        assert name.last_name == "Doe"
        assert name.patronymic is None

    def test_create_name_with_patronymic(self):
        """Создание имени с отчеством."""
        name = Name(first_name="Иван", last_name="Петров", patronymic="Сергеевич")
        assert name.first_name == "Иван"
        assert name.last_name == "Петров"
        assert name.patronymic == "Сергеевич"

    def test_name_strips_whitespace(self):
        """Имя обрезает пробелы по краям."""
        name = Name(first_name="  John  ", last_name="  Doe  ")
        assert name.first_name == "John"
        assert name.last_name == "Doe"

    def test_empty_first_name_raises_error(self):
        """Пустое имя вызывает ошибку."""
        with pytest.raises(ValidationError):
            Name(first_name="", last_name="Doe")

    def test_empty_last_name_raises_error(self):
        """Пустая фамилия вызывает ошибку."""
        with pytest.raises(ValidationError):
            Name(first_name="John", last_name="")

    def test_whitespace_only_name_raises_error(self):
        """Имя из одних пробелов вызывает ошибку."""
        with pytest.raises(ValidationError):
            Name(first_name="   ", last_name="Doe")

    def test_name_too_long_raises_error(self):
        """Имя длиннее 100 символов вызывает ошибку."""
        with pytest.raises(ValidationError):
            Name(first_name="A" * 101, last_name="Doe")

    def test_name_equality(self):
        """Два имени с одинаковыми значениями равны."""
        name1 = Name(first_name="John", last_name="Doe")
        name2 = Name(first_name="John", last_name="Doe")
        assert name1 == name2

    def test_name_with_different_patronymic_not_equal(self):
        """Имена с разными отчествами не равны."""
        name1 = Name(first_name="Иван", last_name="Петров", patronymic="Сергеевич")
        name2 = Name(first_name="Иван", last_name="Петров", patronymic="Александрович")
        assert name1 != name2

    @pytest.mark.parametrize(
        "first_name,last_name,patronymic",
        [
            ("A", "B", None),
            ("John", "Smith", None),
            ("Jean-Pierre", "Dubois", None),
            ("O'Brien", "Connor", None),
            ("Мария", "Иванова", None),
            ("Иван", "Петров", "Сергеевич"),
        ],
    )
    def test_various_valid_names(self, first_name, last_name, patronymic):
        """Различные валидные форматы имен."""
        if patronymic:
            name = Name(
                first_name=first_name, last_name=last_name, patronymic=patronymic
            )
            assert name.patronymic == patronymic
        else:
            name = Name(first_name=first_name, last_name=last_name)

        assert name.first_name == first_name
        assert name.last_name == last_name


class TestHashedPassword:
    def test_create_from_plain_password(self, user_password: str):
        """Создание хешированного пароля из обычного."""
        password = HashedPassword.from_plain_password(user_password)
        assert password.value != user_password

    def test_verify_correct_password(self, user_password: str):
        """Проверка правильного пароля."""
        password = HashedPassword.from_plain_password(user_password)
        assert password.verify(user_password)

    def test_verify_incorrect_password(self, user_password: str):
        """Проверка неправильного пароля."""
        password = HashedPassword.from_plain_password(user_password)
        assert not password.verify("WrongPassword")

    def test_create_from_hash(self, user_password: str):
        """Создание из уже хешированного пароля."""
        hashed = HashedPassword.from_plain_password(user_password)
        password = HashedPassword(value=hashed.value)
        assert password.value == hashed.value
        assert password.verify("StrongPassword123")

    def test_not_enough_symbols(self):
        """Слишком короткий пароль вызывает ошибку."""
        with pytest.raises(WeakPasswordError):
            HashedPassword.from_plain_password("weak")

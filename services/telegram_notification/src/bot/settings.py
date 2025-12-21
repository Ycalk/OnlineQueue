from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Final


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    debug: bool = False

    # Telegram Bot
    bot_token: str

    # PostgreSQL (отдельная БД для telegram_notification)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "telegram_notifications"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    # Redis (для FSM aiogram, если нужно)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # JWT (тот же секрет, что в core)
    secret_key: str
    encoding_algorithm: str = "HS256"

    # RabbitMQ (уже есть в event_processor/settings, но можно дублировать)
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_login: str = "guest"
    rabbitmq_password: str = "guest"


settings: Final[Settings] = Settings()  # type: ignore

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

    bot_token: str

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "telegram_notifications"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    secret_key: str
    encoding_algorithm: str = "HS256"

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_login: str = "guest"
    rabbitmq_password: str = "guest"


settings: Final[Settings] = Settings()

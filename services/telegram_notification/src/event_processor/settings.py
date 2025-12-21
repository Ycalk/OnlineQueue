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

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_login: str = "guest"
    rabbitmq_password: str = "guest"


settings: Final[Settings] = Settings()

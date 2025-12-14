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

    # Тут нужно описать настройки бота:
    # токен, данные для подключения к pg, данные для подключения к redis и прочее


settings: Final[Settings] = Settings()  # type: ignore

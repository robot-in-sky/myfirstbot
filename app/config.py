import logging

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

import app.definitions as _def


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    username: str
    password: str | None = None
    database: str

    @property
    def url(self) -> str:
        return URL.create(
            drivername=f"{_def.DB_SYSTEM}+{_def.DB_DRIVER}",
            username=self.username,
            password=self.password,
            port=self.port,
            host=self.host,
            database=self.database,
        ).render_as_string(hide_password=False)

    echo: bool = False


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    username: str = "default"
    password: str | None = None
    database: int = 0

    ttl_state: int | None = None
    ttl_data: int | None = None


class BotSettings(BaseModel):
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_def.ENVFILE_PATH,
        env_file_encoding=_def.ENVFILE_ENCODING,
        env_nested_delimiter=_def.ENVFILE_DELIMITER,
    )

    debug: bool = False
    log_level: str = "INFO"

    db: DatabaseSettings | None = None
    redis: RedisSettings | None = None
    bot: BotSettings | None = None

    default_admins: set[int] | None = None


settings = Settings()

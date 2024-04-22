import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

from myfirstbot.definitions import ENVFILE_DELIMITER, ENVFILE_ENCODING, ENVFILE_PATH

DB_SYSTEM = "postgresql"
DB_DRIVER = "asyncpg"   # psycopg


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    username: str
    password: str | None = None
    database: str
    database_test: str | None = None

    @property
    def url(self) -> str:
        return URL.create(
            drivername=f"{DB_SYSTEM}+{DB_DRIVER}",
            username=self.username,
            password=self.password,
            port=self.port,
            host=self.host,
            database=self.database,
        ).render_as_string(hide_password=False)


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
        env_file=ENVFILE_PATH,
        env_file_encoding=ENVFILE_ENCODING,
        env_nested_delimiter=ENVFILE_DELIMITER,
    )

    debug: bool = False
    log_level: str = logging.INFO

    db: DatabaseSettings
    redis: RedisSettings
    bot: BotSettings


settings = Settings()


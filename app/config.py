import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


ENVFILE_PATH = Path(__file__).parent.parent.joinpath('.env')
ENVFILE_ENCODING = 'utf-8'
ENVFILE_DELIMITER = '_'


class DatabaseSettings(BaseModel):
    system: str = 'postgresql'
    driver: str = 'asyncpg'

    host: str = 'localhost'
    port: int = 5432
    username: str
    password: str | None = None
    database: str

    @property
    def url(self) -> str:
        return URL.create(
            drivername=f'{self.system}+{self.driver}',
            username=self.username,
            database=self.database,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


class RedisSettings(BaseModel):
    host: str = 'localhost'
    port: int = 6379
    username: str = 'default'
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
        env_nested_delimiter=ENVFILE_DELIMITER
    )

    debug: bool = False
    log_level: str = logging.INFO

    db: DatabaseSettings
    redis: RedisSettings
    bot: BotSettings


settings = Settings()

# print(settings.model_dump())
# print(settings.db.url)


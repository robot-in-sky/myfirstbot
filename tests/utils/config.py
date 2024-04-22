import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

from myfirstbot.config import ENVFILE_DELIMITER, ENVFILE_ENCODING, ENVFILE_PATH, DatabaseSettings


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENVFILE_PATH,
        env_file_encoding=ENVFILE_ENCODING,
        env_nested_delimiter=ENVFILE_DELIMITER,
    )

    debug: bool = False
    log_level: str = logging.INFO

    db: DatabaseSettings


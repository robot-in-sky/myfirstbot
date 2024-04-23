import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from myfirstbot.config import ENVFILE_DELIMITER, ENVFILE_ENCODING, ENVFILE_PATH, DatabaseSettings

TEST_ENVFILE_PATH = Path(ENVFILE_PATH).parent.joinpath(".env.test")


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=TEST_ENVFILE_PATH,
        env_file_encoding=ENVFILE_ENCODING,
        env_nested_delimiter=ENVFILE_DELIMITER,
    )

    debug: bool = False
    log_level: str = logging.INFO

    db: DatabaseSettings


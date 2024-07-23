from pathlib import Path

from alembic.config import Config
from alembic.script import Script
from sqlalchemy import make_url


def test_alembic_config_path(alembic_config: Config) -> None:
    config_file_name = alembic_config.config_file_name
    assert config_file_name
    assert Path(config_file_name).is_file()


def test_alembic_script_location(alembic_config: Config) -> None:
    script_location = alembic_config.get_main_option("script_location")
    assert script_location
    assert Path(script_location).joinpath("env.py").is_file()


def test_alembic_sqlalchemy_url(alembic_config: Config) -> None:
    sqlalchemy_url = alembic_config.get_main_option("sqlalchemy_url")
    assert sqlalchemy_url
    assert make_url(sqlalchemy_url)


def test_alembic_has_revisions(alembic_revisions: list[Script]) -> None:
    assert len(alembic_revisions) > 0

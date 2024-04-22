from pathlib import Path

from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script


def test_alembic_config_path(alembic_config: Config) -> None:
    assert Path(alembic_config.config_file_name).is_file()


def test_alembic_script_location(alembic_config: Config) -> None:
    script_location = alembic_config.get_main_option("script_location")
    assert Path(script_location).joinpath("env.py").is_file()


def test_alembic_sqlalchemy_url(alembic_config: Config) -> None:
    sqlalchemy_url = alembic_config.get_main_option("sqlalchemy.url")
    assert isinstance(sqlalchemy_url, str)


def test_migrations_stairway(
        alembic_config: Config, alembic_revisions: list[Script]
) -> None:
    for revision in alembic_revisions:
        upgrade(alembic_config, revision.revision)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)


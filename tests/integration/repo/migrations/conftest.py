import pytest
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from myfirstbot.config import Settings
from myfirstbot.definitions import APP_DIR
from tests.utils.migrations import get_alembic_config


@pytest.fixture()
def alembic_config(settings: Settings) -> Config:
    return get_alembic_config(
        file_=APP_DIR.joinpath("repo/alembic.ini"),
        db_url=settings.db.url,
    )

@pytest.fixture()
def alembic_revisions(alembic_config: Config) -> list[Script]:
    script_dir = ScriptDirectory.from_config(alembic_config)
    revisions = list(script_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions

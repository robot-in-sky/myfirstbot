import pytest
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from src.paths import SRC_DIR
from src.settings import AppSettings

from tests.utils.migrations import get_alembic_config


@pytest.fixture()
def alembic_config(settings: AppSettings) -> Config:
    return get_alembic_config(
        file_=SRC_DIR.joinpath("alembic.ini"),
        db_url=settings.db.url,
    )

@pytest.fixture()
def alembic_revisions(alembic_config: Config) -> list[Script]:
    script_dir = ScriptDirectory.from_config(alembic_config)
    revisions = list(script_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions

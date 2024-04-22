from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from myfirstbot.definitions import APP_DIR
from tests.utils.alembic import make_alembic_config
from tests.utils.config import TestSettings

ALEMBIC_CONFIG = APP_DIR.joinpath("repositories/postgresql/alembic.ini")


@pytest.fixture()
def alembic_config(settings: TestSettings) -> Config:
    return make_alembic_config(
        db_url=f"{settings.db.url}?async_fallback=True",
        config_file=ALEMBIC_CONFIG,
    )


def alembic_revisions(alembic_config: Config) -> list[Script]:
    script_dir = ScriptDirectory.from_config(alembic_config)
    revisions = list(script_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


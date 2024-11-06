from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script

from tests.utils.migrations import reset_db


def test_migrations_stairway(
    alembic_config: Config, alembic_revisions: list[Script],
) -> None:

    reset_db(alembic_config)

    for revision in alembic_revisions:
        upgrade(alembic_config, revision.revision)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)

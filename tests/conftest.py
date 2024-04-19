"""Configuration for pytest."""
import asyncio

import pytest

from app.config import settings

from .utils.alembic import mocked_alembic_config


@pytest.fixture()
def alembic_config():
    """Alembic configuration object, bound to temporary database."""
    return mocked_alembic_config(settings.db.get_url())


@pytest.fixture()
def event_loop():
    """Fixture for event loop."""
    return asyncio.new_event_loop()

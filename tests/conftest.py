import asyncio

import pytest


@pytest.fixture()
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.new_event_loop()

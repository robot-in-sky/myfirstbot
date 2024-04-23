import pytest
from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from myfirstbot.tgbot.dispatcher import get_dispatcher
from tests.utils.mocked_bot import MockedBot


@pytest.fixture()
def bot() -> MockedBot:
    return MockedBot()


@pytest.fixture()
def storage() -> MemoryStorage:
    return MemoryStorage()


@pytest.fixture()
def dp(storage: BaseStorage) -> Dispatcher:
    return get_dispatcher(storage=storage)

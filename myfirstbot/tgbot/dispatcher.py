from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.strategy import FSMStrategy

from .commands import set_commands
from .middlewares import CurrentUserMiddleware
from .routers import routers


def get_dispatcher(
    storage: BaseStorage,
    fsm_strategy: FSMStrategy | None = FSMStrategy.CHAT,
    event_isolation: BaseEventIsolation | None = None,
) -> Dispatcher:
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation,
    )
    dp.startup.register(set_commands)
    dp.update.outer_middleware(CurrentUserMiddleware())
    dp.include_routers(*routers)

    return dp


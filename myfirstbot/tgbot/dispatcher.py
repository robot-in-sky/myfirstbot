from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.strategy import FSMStrategy

from .handlers import routers
from .middlewares.current_user import CurrentUserMiddleware


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

    for router in routers:
        dp.include_router(router)

    dp.update.outer_middleware(CurrentUserMiddleware())

    return dp

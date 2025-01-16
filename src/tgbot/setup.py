from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis

from src.io.redis import RedisSettings

from .commands import set_commands
from .middlewares import CurrentUserMiddleware
from .routers import routers
from .tgbot_settings import TgBotSettings


def setup_tgbot(tgbot_settings: TgBotSettings,
                redis_settings: RedisSettings) -> tuple[Bot, Dispatcher]:

    bot = Bot(token=tgbot_settings.token,
               default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    redis_database = tgbot_settings.redis_storage.database
    if redis_database is None:
        redis_database = redis_settings.database

    redis = Redis(port=redis_settings.port,
                  host=redis_settings.host,
                  username=redis_settings.username,
                  password=redis_settings.password,
                  db=redis_database)

    storage = RedisStorage(redis=redis,
                           state_ttl=tgbot_settings.redis_storage.state_ttl,
                           data_ttl=tgbot_settings.redis_storage.data_ttl,
                           key_builder=DefaultKeyBuilder(with_destiny=True))

    dp = Dispatcher(storage=storage,
                    fsm_strategy=FSMStrategy.CHAT)

    dp.startup.register(set_commands)
    dp.update.outer_middleware(CurrentUserMiddleware())
    dp.include_routers(*routers)
    return bot, dp

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis

from clients.redis import RedisSettings
from interfaces.tgbot.tgbot_deps import TgBotDependencies
from settings.tgbot_settings import TgBotSettings

from .commands import set_commands
from .middlewares import CurrentUserMiddleware
from .routers import routers


class TgBotApplication:

    def __init__(self, tgbot_settings: TgBotSettings,
                       redis_settings: RedisSettings) -> None:

        self.bot = Bot(token=tgbot_settings.token,
                       default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        redis_database = tgbot_settings.redis.database
        if redis_database is None:
            redis_database = redis_settings.database

        redis = Redis(port=redis_settings.port,
                      host=redis_settings.host,
                      username=redis_settings.username,
                      password=redis_settings.password,
                      db=redis_database)

        storage = RedisStorage(redis=redis,
                               state_ttl=tgbot_settings.redis.state_ttl,
                               data_ttl=tgbot_settings.redis.data_ttl,
                               key_builder=DefaultKeyBuilder(with_destiny=True))

        self.dp = Dispatcher(storage=storage,
                             fsm_strategy=FSMStrategy.CHAT)

        self.dp.startup.register(set_commands)
        self.dp.update.outer_middleware(CurrentUserMiddleware())
        self.dp.include_routers(*routers)


    async def start(self, deps: TgBotDependencies) -> None:
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot,
                                    allowed_updates=self.dp.resolve_used_update_types(),
                                    deps=deps)

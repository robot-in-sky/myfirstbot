import asyncio
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from src.config import settings
from src.repo.utils.database import Database
from src.tgbot.dispatcher import get_dispatcher

bot = Bot(token=settings.bot.token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = RedisStorage(
    redis=Redis(
        port=settings.redis.port,
        host=settings.redis.host,
        db=settings.redis.database,
        username=settings.redis.username,
        password=settings.redis.password,
    ),
    state_ttl=settings.redis.ttl_state,
    data_ttl=settings.redis.ttl_data,
    key_builder=DefaultKeyBuilder(with_destiny=True),
)

dp = get_dispatcher(storage=storage)

async def start_bot() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           allowed_updates=dp.resolve_used_update_types(),
                           db=Database(settings.db))


if __name__ == "__main__":
    logging.basicConfig(level=settings.log_level)
    """logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")"""
    asyncio.run(start_bot())

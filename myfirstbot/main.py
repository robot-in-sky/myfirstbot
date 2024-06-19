import asyncio
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from myfirstbot.config import settings
from myfirstbot.repo.utils.database import Database
from myfirstbot.tgbot.dispatcher import get_dispatcher


async def start_bot() -> None:
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    )
    await bot.delete_webhook(drop_pending_updates=True)

    dp = get_dispatcher(
        storage=RedisStorage(
            redis=Redis(
                port=settings.redis.port,
                host=settings.redis.host,
                db=settings.redis.database,
                username=settings.redis.username,
                password=settings.redis.password,
            ),
            state_ttl=settings.redis.ttl_state,
            data_ttl=settings.redis.ttl_data,
        ),
    )
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        db=Database(settings.db),
    )


if __name__ == "__main__":
    logging.basicConfig(level=settings.log_level)
    asyncio.run(start_bot())

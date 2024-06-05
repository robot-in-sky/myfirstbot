import asyncio
import logging

from aiogram import Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from redis.asyncio.client import Redis

from myfirstbot.config import settings
from myfirstbot.repo.utils.database import Database
from myfirstbot.tgbot.dispatcher import get_dispatcher


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="forms", description="Мои анкеты"),
            BotCommand(command="help", description="Помощь"),
        ],
    )


async def start_bot() -> None:
    db = Database(settings.db)
    bot = Bot(token=settings.bot.token)
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
    dp.startup.register(set_commands)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        db=db,
    )


if __name__ == "__main__":
    logging.basicConfig(level=settings.log_level)
    asyncio.run(start_bot())

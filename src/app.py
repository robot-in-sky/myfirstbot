import logging

from aio_pika.patterns import JsonRPC

from src.deps import Dependencies
from src.io.amqp import AMQPClient
from src.io.database import DatabaseClient
from src.io.redis import RedisClient
from src.io.s3 import S3Client
from src.settings import AppSettings, LogSettings
from src.tgbot.setup import setup_tgbot


class Application:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

        self.configure_logging(settings.log)

        self.deps = Dependencies(
            settings=self.settings,
            db=DatabaseClient(settings.db),
            redis=RedisClient(settings.redis),
            s3=S3Client(settings.s3))


    @staticmethod
    def configure_logging(settings: LogSettings) -> None:
        logging.basicConfig(level=settings.level)


    async def start(self) -> None:
        amqp = AMQPClient(self.settings.amqp)
        connection = await amqp.get_connection()
        channel = await connection.channel()
        self.deps.rpc = await JsonRPC.create(channel)

        try:
            bot, dp = setup_tgbot(tgbot_settings=self.settings.tgbot,
                                  redis_settings=self.settings.redis)

            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot,
                                   allowed_updates=dp.resolve_used_update_types(),
                                   deps=self.deps)
        finally:
            await connection.close()

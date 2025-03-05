import logging

from aio_pika.patterns import JsonRPC

from src.deps import Dependencies
from src.infrastructure.amqp import AMQPClient
from src.infrastructure.database import DatabaseClient
from src.infrastructure.redis import RedisClient
from src.infrastructure.s3 import S3Client
from src.settings import AppSettings, LogSettings
from src.tgbot.tgbot_app import TgBotApplication


class Application:
    def __init__(self, settings: AppSettings) -> None:
        self.configure_logging(settings.log)
        self.settings = settings
        self.deps = None
        self.tgbot = TgBotApplication(tgbot_settings=settings.tgbot,
                                      redis_settings=settings.redis)

    @staticmethod
    def configure_logging(settings: LogSettings) -> None:
        logging.basicConfig(level=settings.level)


    async def start(self) -> None:
        db = DatabaseClient(self.settings.db)
        await db.add_uuid_extension()

        amqp = AMQPClient(self.settings.amqp)
        connection = await amqp.get_connection()
        channel = await connection.channel()
        rpc = await JsonRPC.create(channel)

        self.deps = Dependencies(settings=self.settings,
                                 db=db,
                                 redis=RedisClient(self.settings.redis),
                                 s3=S3Client(self.settings.s3),
                                 rpc=rpc)

        try:
            await self.tgbot.start(self.deps)
        finally:
            await connection.close()

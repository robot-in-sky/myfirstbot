import logging

from aio_pika.patterns import JsonRPC

from clients.amqp import AMQPClient
from clients.database import DatabaseClient
from clients.redis import RedisClient
from clients.s3 import S3Client
from interfaces.tgbot import TgBotApplication
from interfaces.tgbot.tgbot_deps import TgBotDependencies
from settings import AppSettings, LogSettings


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

        self.deps = TgBotDependencies(settings=self.settings,
                                      db=db,
                                      redis=RedisClient(self.settings.redis),
                                      s3=S3Client(self.settings.s3),
                                      rpc=rpc)

        try:
            await self.tgbot.start(self.deps)
        finally:
            await connection.close()

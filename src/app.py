import logging

from aio_pika.patterns import JsonRPC

from src.deps import Dependencies
from src.io.amqp import AMQPClient
from src.settings import AppSettings, LogSettings
from src.tgbot.tgbot_init import tgbot_init


class Application:
    def __init__(self, settings: AppSettings) -> None:
        self.configure_logging(settings.log)
        self.settings = settings
        self.deps = Dependencies(settings)

    @staticmethod
    def configure_logging(settings: LogSettings) -> None:
        logging.basicConfig(level=settings.level)


    async def start(self) -> None:
        amqp = AMQPClient(self.settings.amqp)
        connection = await amqp.get_connection()
        channel = await connection.channel()
        rpc = await JsonRPC.create(channel)
        self.deps.post_init(rpc)

        try:
            bot, dp = tgbot_init(tgbot_settings=self.settings.tgbot,
                                 redis_settings=self.settings.redis)

            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot,
                                   allowed_updates=dp.resolve_used_update_types(),
                                   deps=self.deps)
        finally:
            await connection.close()

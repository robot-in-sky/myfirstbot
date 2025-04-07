import aio_pika

from .amqp_settings import AMQPSettings


class AMQPClient:

    def __init__(self, settings: AMQPSettings) -> None:
        self.settings = settings


    async def get_connection(self) -> aio_pika.abc.AbstractRobustConnection:
        # TODO: Handle AMQPConnectionError
        return await aio_pika.connect_robust(
            url=self.settings.url,
            reconnect_interval=self.settings.reconnect_interval)

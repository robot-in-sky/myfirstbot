from src.clients.amqp import AMQPSettings
from src.clients.database import DatabaseSettings
from src.clients.redis import RedisSettings
from src.clients.s3 import S3Settings
from src.settings.app_settings_base import AppSettingsBase
from src.settings.log_settings import LogSettings
from src.tgbot.tgbot_settings import TgBotSettings


class AppSettings(AppSettingsBase):

    # Required settings
    db: DatabaseSettings
    redis: RedisSettings
    tgbot: TgBotSettings
    amqp: AMQPSettings
    s3: S3Settings

    # Optional settings
    log: LogSettings = LogSettings()
    default_admins: set[int] | None = [999999999]  # noqa: RUF012


if __name__ == "__main__":
    AppSettings.save_dotenv_example()

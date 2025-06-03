from .amqp_settings import AMQPSettings
from .base.app_settings_base import AppSettingsBase
from .database_settings import DatabaseSettings
from .log_settings import LogSettings
from .redis_settings import RedisSettings
from .s3_settings import S3Settings
from .tgbot_settings import TgBotSettings


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

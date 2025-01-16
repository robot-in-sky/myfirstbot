from pydantic import BaseModel


class RedisStorageSettings(BaseModel):
    database: int | None = None
    state_ttl: int | None = None
    data_ttl: int | None = None


class TgBotSettings(BaseModel):
    token: str
    redis_storage: RedisStorageSettings = RedisStorageSettings()

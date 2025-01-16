from pydantic import BaseModel


class RedisSettings(BaseModel):
    host: str
    port: int = 6379
    username: str = "default"
    password: str | None = None
    database: int = 0

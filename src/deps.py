from dataclasses import dataclass

from aio_pika.patterns import JsonRPC

from src.io.database import DatabaseClient
from src.io.redis import RedisClient
from src.io.s3 import S3Client
from src.settings import AppSettings


@dataclass
class Dependencies:
    settings: AppSettings
    db: DatabaseClient
    redis: RedisClient
    s3: S3Client
    rpc: JsonRPC | None = None

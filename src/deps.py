from aio_pika.patterns import JsonRPC

from src.entities.user import User
from src.io.database import DatabaseClient
from src.io.redis import RedisClient
from src.io.s3 import S3Client
from src.services import AttachmentService, AuthService, FormService, OrderService, UserService
from src.settings import AppSettings


class Dependencies:

    def __init__(self, settings: AppSettings) -> None:
        self._db = DatabaseClient(settings.db)
        self._redis = RedisClient(settings.redis)
        self._s3 = S3Client(settings.s3)
        self._auth = AuthService(self._db)
        self._attachments = AttachmentService(self._s3)
        self._forms = FormService()
        self._rpc = None

    def post_init(self, rpc: JsonRPC) -> None:
        self._rpc = rpc

    """
    @property
    def db(self) -> DatabaseClient:
        return self._db

    @property
    def redis(self) -> RedisClient:
        return self._redis

    @property
    def s3(self) -> S3Client:
        return self._s3
    """

    @property
    def rpc(self) -> JsonRPC:
        if self._rpc is None:
            message = "RPC is not initialized"
            raise RuntimeError(message)
        return self._rpc

    @property
    def attachments(self) -> AttachmentService:
        return self._attachments

    @property
    def auth(self) -> AuthService:
        return self._auth

    @property
    def forms(self) -> FormService:
        return self._forms

    def users(self, current_user: User) -> UserService:
        return UserService(self._db, current_user)

    def orders(self, current_user: User) -> OrderService:
        return OrderService(self._db, current_user)

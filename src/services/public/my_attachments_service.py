from uuid import UUID

from src.entities.users import User
from src.exceptions import AccessDeniedError
from src.infrastructure.database import DatabaseClient
from src.infrastructure.s3 import S3Client
from src.repositories import AppFormRepo


class MyAttachmentsService:

    def __init__(self, s3: S3Client, db: DatabaseClient, current_user: User) -> None:
        self._s3 = s3
        self._app_form_repo = AppFormRepo(db)
        self.current_user = current_user

    # User has access only to attachments with the same id as his application form
    async def _check_form_exists(self, id_: UUID) -> None:
        if form := await self._app_form_repo.get(id_):  # noqa: SIM102
            if form.user_id == self.current_user.id:
                return
        raise AccessDeniedError

    @staticmethod
    def _get_object_name(id_: UUID, basename: str) -> str:
        return f"{id_}/{basename}"


    async def add_bytes(self, id_: UUID, basename: str, data: bytes) -> str:
        # await self._check_form_exists(id_)
        obj_name = self._get_object_name(id_, basename)
        await self._s3.put_object(obj_name, data)
        return obj_name


    async def get_bytes(self, id_: UUID, basename: str) -> bytes:
        # await self._check_form_exists(id_)
        obj_name = self._get_object_name(id_, basename)
        return await self._s3.get_object(obj_name)


    async def delete(self, id_: UUID, basename: str) -> None:
        # await self._check_form_exists(id_)
        obj_name = self._get_object_name(id_, basename)
        await self._s3.delete_object(obj_name)

from uuid import UUID

from src.clients.s3 import S3Client
from src.entities.users import User, UserRole
from src.services.utils.access_level import access_level


class AttachmentService:

    def __init__(self, s3: S3Client, current_user: User) -> None:
        self._s3 = s3
        self.current_user = current_user

    @staticmethod
    def _get_object_name(id_: str | UUID, basename: str) -> str:
        return f"{id_}/{basename}"


    @access_level(required=UserRole.AGENT)
    async def add_bytes(self, id_: str | UUID, basename: str, data: bytes) -> str:
        obj_name = self._get_object_name(id_, basename)
        await self._s3.put_object(obj_name, data)
        return obj_name


    @access_level(required=UserRole.AGENT)
    async def get_bytes(self, id_: str | UUID, basename: str) -> bytes:
        obj_name = self._get_object_name(id_, basename)
        return await self._s3.get_object(obj_name)


    @access_level(required=UserRole.AGENT)
    async def delete(self, id_: str | UUID, basename: str) -> None:
        obj_name = self._get_object_name(id_, basename)
        await self._s3.delete_object(obj_name)

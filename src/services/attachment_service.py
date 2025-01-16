from src.deps import Dependencies


class AttachmentService:

    def __init__(self, deps: Dependencies) -> None:
        self.s3 = deps.s3

    async def add_bytes(self, group_id: str, filename: str, data: bytes) -> str:
        obj_name = self._get_object_name(group_id, filename)
        await self.s3.put_object(obj_name, data)
        return obj_name

    async def get_bytes(self, group_id: str, filename: str) -> bytes:
        obj_name = self._get_object_name(group_id, filename)
        return await self.s3.get_object(obj_name)

    async def delete(self, group_id: str, filename: str) -> None:
        obj_name = self._get_object_name(group_id, filename)
        await self.s3.delete_object(obj_name)

    @staticmethod
    def _get_object_name(group_id: str, filename: str) -> str:
        return f"{group_id}/{filename}"

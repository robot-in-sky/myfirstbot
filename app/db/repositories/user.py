from sqlalchemy.ext.asyncio import AsyncSession

from .abs_repo import AbstractRepo
from .abs_orm_repo import AbstractOrmRepo
from .exc_mapper import exception_mapper

from ..models.user import UserModel
from ..schemas.user import UserSchemaAdd, UserSchema
from ..types.access_level import AccessLevel


class UserRepo(AbstractRepo[UserSchema]):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.orm = AbstractOrmRepo[UserModel](session=session, model=UserModel)

    @exception_mapper
    async def add(self, instance: UserSchemaAdd) -> UserSchema:
        instance = await self.orm.add(**instance.model_dump())
        return UserSchema.model_validate(instance)

    @exception_mapper
    async def get(self, ident: int) -> UserSchema | None:
        instance = await self.orm.get(ident)
        return UserSchema.model_validate(instance) if instance else None

    @exception_mapper
    async def get_one(self, **filter_by) -> UserSchema | None:
        instance = await self.orm.get_one(**filter_by)
        return UserSchema.model_validate(instance) if instance else None

    @exception_mapper
    async def get_many(
            self, skip: int = 0, limit: int = 100, order_by=None, **filter_by
    ) -> list[UserSchema]:
        instances = await self.orm.get_many(
            skip=skip, limit=limit, order_by=order_by, **filter_by
        )
        return list(map(UserSchema.model_validate, instances))

    @exception_mapper
    async def update(self, ident: int, **attrs) -> UserSchema | None:
        for k, v in attrs.items():
            UserSchema.__pydantic_validator__.validate_assignment(
                UserSchema.model_construct(), k, v
            )
        instance = await self.orm.update(ident=ident, **attrs)
        return UserSchema.model_validate(instance) if instance else None

    @exception_mapper
    async def delete(self, ident: int) -> None:
        await self.orm.delete(ident)

    async def get_one_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        return await self.get_one(telegram_id=telegram_id)

    async def update_info(
            self, ident: int,
            user_name: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            chat_id: int | None = None
    ) -> UserSchema | None:
        kwargs = {
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'chat_id': chat_id
        }
        return await self.update(ident, **kwargs)

    async def set_access_level(
            self, ident: int, access_level: AccessLevel
    ) -> UserSchema | None:
        return await self.update(ident, access_level=access_level)

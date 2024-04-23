from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.repositories.sqlalchemy.abs_repo import AbstractRepo
from myfirstbot.base.repositories.sqlalchemy.exc_mapper import exception_mapper
from myfirstbot.entities.enums.access_level import AccessLevel
from myfirstbot.entities.user import User, UserCreate, UserUpdate
from myfirstbot.repositories.postgresql.models.user import User as _UserOrm


class UserRepo(AbstractRepo[User, UserCreate, UserUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @exception_mapper
    async def add(self, instance: UserCreate) -> User:
        values = instance.model_dump()
        query = insert(_UserOrm).values(**values).returning(_UserOrm)
        result = await self.session.execute(query)
        await self.session.commit()
        return User.model_validate(result)

    @exception_mapper
    async def get(self, id_: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.id == id_)
        result = await self.session.scalar(query)
        return User.model_validate(result) if result else None

    @exception_mapper
    async def update(self, id_: int, instance: UserUpdate) -> User:
        values = instance.model_dump()
        query = (update(_UserOrm).where(_UserOrm.id == id_)
                 .values(**values).returning(_UserOrm))
        result = await self.session.execute(query)
        await self.session.commit()
        return User.model_validate(result)

    @exception_mapper
    async def delete(self, id_: int) -> None:
        query = delete(_UserOrm).where(_UserOrm.id == id_)
        await self.session.execute(query)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.telegram_id == telegram_id)
        result = await self.session.scalar(query)
        return User.model_validate(result) if result else None

    async def update_telegram_info(  # noqa: PLR0913
            self, id_: int,
            user_name: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            chat_id: int | None = None,
    ) -> User | None:
        return await self.update(id_, UserUpdate(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            chat_id=chat_id
        ))

    async def set_access_level(
            self, id_: int, access_level: AccessLevel,
    ) -> User | None:
        return await self.update(id_, UserUpdate(access_level=access_level))


"""
    @exception_mapper
    async def get_many(
            self, skip: int = 0, limit: int = 100, order_by=None, **filter_by,
    ) -> list[User]:
        instances = await self.orm.get_many(
            skip=skip, limit=limit, order_by=order_by, **filter_by,
        )
        return list(map(UserSchema.model_validate, instances)
"""

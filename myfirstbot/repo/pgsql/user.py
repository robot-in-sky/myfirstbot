from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.entities.filters import QueryFilter
from myfirstbot.base.repo.sql.abs_repo import AbstractRepo
from myfirstbot.base.repo.sql.exc_mapper import exception_mapper
from myfirstbot.base.repo.sql.query_utils import apply_filter
from myfirstbot.entities.user import User, UserCreate, UserUpdate
from myfirstbot.repo.pgsql.models.user import User as _UserOrm


class UserRepo(AbstractRepo[User, UserCreate, UserUpdate]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @exception_mapper
    async def add(self, instance: UserCreate) -> User:
        query = (insert(_UserOrm).values(**instance.model_dump())
                 .returning(_UserOrm))
        result = await self.session.scalar(query)
        await self.session.commit()
        return User.model_validate(result)


    async def get(self, id_: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.id == id_)
        result = await self.session.scalar(query)
        return User.model_validate(result) if result else None

    @exception_mapper
    async def update(self, id_: int, instance: UserUpdate) -> User:
        query = (update(_UserOrm).where(_UserOrm.id == id_)
                 .values(**instance.model_dump()).returning(_UserOrm))
        result = await self.session.scalar(query)
        await self.session.commit()
        return User.model_validate(result)

    async def delete(self, id_: int) -> None:
        query = delete(_UserOrm).where(_UserOrm.id == id_)
        await self.session.execute(query)
        await self.session.commit()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.telegram_id == telegram_id)
        result = await self.session.scalar(query)
        return User.model_validate(result) if result else None

    async def get_one(self, filter_: QueryFilter) -> User | None:
        query = apply_filter(select(_UserOrm), filter_)
        result = await self.session.scalar(query)
        return User.model_validate(result) if result else None

    async def get_all(
            self, filter_: QueryFilter, *,
            skip: int = 0, limit: int = -1, order_by: str | None = None
    ) -> list[User]:
        query = apply_filter(select(_UserOrm), filter_)
        if limit > 0:
            query = query.offset(skip).limit(limit)
        if order_by:
            query = query.order_by(order_by)
        result = (await self.session.scalars(query)).all()
        return list(map(User.model_validate, result))

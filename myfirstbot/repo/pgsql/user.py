from collections.abc import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.entities.query import Pagination, QueryFilter, Sorting
from myfirstbot.base.repo.sql.abs_repo import AbstractRepo
from myfirstbot.base.repo.sql.exc_mapper import exception_mapper
from myfirstbot.base.repo.sql.query_utils import apply_filters, apply_pagination, apply_sorting
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

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.telegram_id == telegram_id)
        result = await self.session.scalar(query)
        return User.model_validate(result) if result else None

    async def get_many(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> list[User]:
        query = select(_UserOrm)
        if filters:
            query = apply_filters(query, filters, or_=or_)
        if sorting:
            query = apply_sorting(query, sorting)
        if pagination:
            query = apply_pagination(query, pagination)
        result = (await self.session.scalars(query)).all()
        return list(map(User.model_validate, result))


    async def update(self, id_: int, instance: UserUpdate) -> User | None:
        query = (update(_UserOrm).where(_UserOrm.id == id_)
                 .values(**instance.model_dump()).returning(_UserOrm))
        result = await self.session.scalar(query)
        if result:
            await self.session.commit()
            return User.model_validate(result)
        return None


    async def delete(self, id_: int) -> int | None:
        query = delete(_UserOrm).where(_UserOrm.id == id_).returning(_UserOrm.id)
        result = await self.session.scalar(query)
        if result:
            await self.session.commit()
            return result
        return None

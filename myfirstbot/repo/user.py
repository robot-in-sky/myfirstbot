from collections.abc import Sequence
from datetime import UTC, datetime
from math import ceil

from pydantic import TypeAdapter
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.query import Pagination, QueryFilter, QueryResult, Sorting
from myfirstbot.entities.user import User, UserAdd, UserUpdate
from myfirstbot.repo.base import AbstractRepo
from myfirstbot.repo.models import User as _UserOrm
from myfirstbot.repo.utils import Database, exception_mapper
from myfirstbot.repo.utils.query_utils import apply_filters, apply_pagination, apply_sorting, row_count


class UserRepo(AbstractRepo[User, UserAdd, UserUpdate]):

    def __init__(self, database: Database) -> None:
        self.db = database

    @exception_mapper
    async def add(self, instance: UserAdd) -> User:
        query = (insert(_UserOrm).values(**instance.model_dump())
                     .returning(_UserOrm))
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            await session.commit()
            return User.model_validate(result)

    async def get(self, id_: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.id == id_)
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                return User.model_validate(result)
            return None

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        query = select(_UserOrm).where(_UserOrm.telegram_id == telegram_id)
        async with self.db.get_session() as session:
            result = await session.scalar(query)
            return User.model_validate(result) if result else None

    async def get_many(
            self,
            filters: Sequence[QueryFilter] | None = None,
            *,
            or_: bool = False,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> QueryResult[User]:
        query = select(_UserOrm)
        if filters:
            query = apply_filters(query, filters, or_=or_)
        if sorting:
            query = apply_sorting(query, sorting)

        async with self.db.get_session() as session:
            total_items = await row_count(session, query)

            page, per_page, total_pages = None, None, None

            if pagination and total_items > 0:
                query = apply_pagination(query, pagination)
                page = pagination.page
                per_page = pagination.per_page
                total_pages = ceil(total_items / pagination.per_page)

            orm_items = (await session.scalars(query)).all()
            items = TypeAdapter(list[User]).validate_python(orm_items)

            return QueryResult[User](
                items=items,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                total_items=total_items,
            )

    async def update(self, id_: int, instance: UserUpdate) -> User | None:
        query = (update(_UserOrm).where(_UserOrm.id == id_)
                 .values(**instance.model_dump(), updated=datetime.now(UTC))
                 .returning(_UserOrm))
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                await session.commit()
                return User.model_validate(result)
            return None

    async def delete(self, id_: int) -> int | None:
        query = delete(_UserOrm).where(_UserOrm.id == id_).returning(_UserOrm.id)
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                await session.commit()
                return result
            return None

    async def set_role(self, id_: int, role: UserRole) -> int | None:
        query = (update(_UserOrm).where(_UserOrm.id == id_)
                 .values(role=role, updated=datetime.now(UTC))
                 .returning(_UserOrm.id))
        async with self.db.get_session() as session:
            if result := await session.scalar(query):
                await session.commit()
                return result
            return None
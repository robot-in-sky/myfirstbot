from collections.abc import Sequence
from datetime import UTC, datetime
from math import ceil

from pydantic import TypeAdapter
from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert

from app.entities.choices import UserRole
from app.entities.query import CountResultItem, Pagination, QueryFilter, QueryResult, Search, Sorting
from app.entities.user import User, UserAdd, UserUpdate
from app.repo.base import AbstractRepo
from app.repo.models import OrmUser
from app.repo.utils import Database, exception_mapper
from app.repo.utils.query_utils import apply_filters, apply_pagination, apply_search, apply_sorting, get_count


class UserRepo(AbstractRepo[User, UserAdd, UserUpdate]):

    def __init__(self, database: Database) -> None:
        self.db = database

    @exception_mapper
    async def add(self, instance: UserAdd) -> User:
        stmt = (insert(OrmUser).values(**instance.model_dump())
                     .returning(OrmUser))
        async with self.db.get_session() as session:
            result = await session.scalar(stmt)
            await session.commit()
            return User.model_validate(result)

    async def get(self, id_: int) -> User | None:
        stmt = select(OrmUser).where(OrmUser.id == id_)
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                return User.model_validate(result)
            return None

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(OrmUser).where(OrmUser.telegram_id == telegram_id)
        async with self.db.get_session() as session:
            result = await session.scalar(stmt)
            return User.model_validate(result) if result else None

    async def update(self, id_: int, instance: UserUpdate) -> User | None:
        stmt = (update(OrmUser).where(OrmUser.id == id_)
                 .values(**instance.model_dump(), updated=datetime.now(UTC))
                 .returning(OrmUser))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return User.model_validate(result)
            return None

    async def delete(self, id_: int) -> int | None:
        stmt = delete(OrmUser).where(OrmUser.id == id_).returning(OrmUser.id)
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None

    async def set_role(self, id_: int, role: UserRole) -> int | None:
        stmt = (update(OrmUser).where(OrmUser.id == id_)
                 .values(role=role, updated=datetime.now(UTC))
                 .returning(OrmUser.id))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None

    async def get_all(  # noqa: PLR0913
            self,
            filters: Sequence[QueryFilter] | None = None,
            search: Search | None = None,
            *,
            or_: bool = False,
            sorting: Sorting | None = None,
            pagination: Pagination | None = None,
    ) -> QueryResult[User]:
        stmt = select(OrmUser)
        if filters:
            stmt = apply_filters(stmt, filters, or_=or_)
        if search:
            stmt = apply_search(stmt, search)

        async with self.db.get_session() as session:
            total_items = await get_count(session, stmt)

            if sorting:
                stmt = apply_sorting(stmt, sorting)

            page, per_page, total_pages = None, None, None

            if pagination and total_items > 0:
                stmt = apply_pagination(stmt, pagination)
                page = pagination.page
                per_page = pagination.per_page
                total_pages = ceil(total_items / pagination.per_page)

            orm_items = (await session.scalars(stmt)).all()
            items = TypeAdapter(list[User]).validate_python(orm_items)

            return QueryResult[User](
                items=items,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                total_items=total_items,
            )

    async def get_count(
            self,
            filters: Sequence[QueryFilter] | None = None,
            search: Search | None = None,
            *,
            or_: bool = False,
    ) -> int:
        stmt = select(OrmUser)
        if filters:
            stmt = apply_filters(stmt, filters, or_=or_)
        if search:
            stmt = apply_search(stmt, search)

        async with self.db.get_session() as session:
            return await get_count(session, stmt)

    async def get_count_by_role(
            self,
            filters: Sequence[QueryFilter] | None = None,
            search: Search | None = None,
            *,
            or_: bool = False,
    ) -> list[CountResultItem[UserRole]]:
        column = OrmUser.role
        stmt = select(column, func.count(column))
        if filters:
            stmt = apply_filters(stmt, filters, or_=or_)
        if search:
            stmt = apply_search(stmt, search)
        stmt = stmt.group_by(column).order_by(column)

        async with self.db.get_session() as session:
            result = (await session.execute(stmt)).all()
            return [CountResultItem[UserRole](
                value=item[0], count=item[1],
            ) for item in result]

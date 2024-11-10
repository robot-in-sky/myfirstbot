from datetime import datetime
from math import ceil

from pydantic import TypeAdapter
from pytz import UTC
from sqlalchemy import Select, and_, delete, func, select, update
from sqlalchemy.dialects.postgresql import insert

from src.entities.base import QueryCountItem, QueryResult
from src.entities.choices import UserRole
from src.entities.user import USER_SEARCH_BY, User, UserAdd, UserQuery, UserQueryPaged, UserUpdate
from src.repositories.base import AbstractRepo
from src.repositories.models import OrmUser
from src.repositories.utils import Database, exception_mapper
from src.repositories.utils.query_utils import (
    apply_pagination,
    apply_search,
    apply_sorting,
    get_column,
    get_row_count,
    match_types,
)


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
                 .values(**instance.model_dump(), updated_at=datetime.now(UTC))
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
                 .values(role=role, updated_at=datetime.now(UTC))
                 .returning(OrmUser.id))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None

    """
        role: UserRole | None = None
        role__in: set[UserRole] | None = None
        search: str | None = None
    """
    @staticmethod
    def _apply_filters(
            stmt: Select[tuple[OrmUser]],
            query: UserQuery,
    ) -> Select[tuple[OrmUser]]:
        clauses = []
        if query.role is not None:
            column = get_column(stmt, "role")
            clauses.append(column == query.role)
        if query.role__in is not None:
            column = get_column(stmt, "role")
            values = match_types(query.role__in, column)
            clauses.append(column.in_(values))
        stmt = stmt.where(and_(*clauses))

        if query.search is not None:
            stmt = apply_search(stmt, query.search, USER_SEARCH_BY)

        return stmt


    async def get_many(self, query: UserQueryPaged) -> QueryResult[User]:
        stmt = select(OrmUser)
        stmt = self._apply_filters(stmt, query)

        async with self.db.get_session() as session:
            total_items = await get_row_count(session, stmt)

            if query.sort_by is not None:
                stmt = apply_sorting(stmt, query.sort_by, query.sort)

            items, page, per_page, total_pages = [], None, None, None

            if query.page > 0 and query.per_page > 0 and total_items > 0:
                stmt = apply_pagination(stmt, query.page, query.per_page)
                orm_items = (await session.scalars(stmt)).all()
                items = TypeAdapter(list[User]).validate_python(orm_items)

                page = query.page
                per_page = query.per_page
                total_pages = ceil(total_items / query.per_page)

            return QueryResult[User](
                items=items,
                page=page,
                per_page=per_page,
                total_pages=total_pages,
                total_items=total_items,
            )

    async def get_count(self, query: UserQuery) -> int:
        stmt = select(OrmUser)
        stmt = self._apply_filters(stmt, query)

        async with self.db.get_session() as session:
            return await get_row_count(session, stmt)

    async def get_count_by_role(self, query: UserQuery) -> list[QueryCountItem[UserRole]]:
        column = OrmUser.role
        stmt = select(column, func.count(column))
        query.role = None
        query.role__in = None
        stmt = self._apply_filters(stmt, query)
        stmt = stmt.group_by(column).order_by(column)

        async with self.db.get_session() as session:
            result = (await session.execute(stmt)).all()
            return [QueryCountItem[UserRole](
                value=item[0], count=item[1],
            ) for item in result]

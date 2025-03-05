from datetime import datetime
from math import ceil
from uuid import UUID

from pydantic import TypeAdapter
from pytz import UTC
from sqlalchemy import Select, and_, delete, func, select, update
from sqlalchemy.dialects.postgresql import insert

from src.entities.base import QueryCountItem, QueryResult
from src.entities.visas import AppFormStatus
from src.entities.visas.app_form import (
    AppForm,
    AppFormAdd,
    AppFormQuery,
    AppFormQueryPaged,
    AppFormUpdate,
)
from src.infrastructure.database import DatabaseClient
from src.orm_models import OrmAppForm
from src.repositories.utils import exception_mapper
from src.repositories.utils.query_utils import (
    apply_pagination,
    apply_sorting,
    get_row_count,
    match_types,
)


class AppFormRepo:

    def __init__(self, db: DatabaseClient) -> None:
        self.db = db


    @exception_mapper
    async def add(self, instance: AppFormAdd) -> AppForm:
        stmt = (insert(OrmAppForm).values(**instance.model_dump())
                .returning(OrmAppForm))
        async with self.db.get_session() as session:
            result = await session.scalar(stmt)
            await session.commit()
            return AppForm.model_validate(result)


    async def get(self, id_: UUID) -> AppForm | None:
        stmt = select(OrmAppForm).where(OrmAppForm.id == id_)
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                return AppForm.model_validate(result)
            return None


    async def update(self, id_: UUID, instance: AppFormUpdate) -> AppForm | None:
        stmt = (update(OrmAppForm).where(OrmAppForm.id == id_)
                .values(**instance.model_dump(), updated_at=datetime.now(UTC))
                .returning(OrmAppForm))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return AppForm.model_validate(result)
            return None


    async def delete(self, id_: UUID) -> UUID | None:
        stmt = delete(OrmAppForm).where(OrmAppForm.id == id_).returning(OrmAppForm.id)
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None


    async def set_status(self, id_: UUID, status: AppFormStatus) -> UUID | None:
        stmt = (update(OrmAppForm).where(OrmAppForm.id == id_)
                .values(status=status, updated_at=datetime.now(UTC))
                .returning(OrmAppForm.id))
        async with self.db.get_session() as session:
            if result := await session.scalar(stmt):
                await session.commit()
                return result
            return None


    """
        user_id: int | None = None
        country: Country | None = None
        country__in: set[Country] | None = None
        status: AppFormStatus | None = None
        status__in: set[AppFormStatus] | None = None
        status__not_in: set[AppFormStatus] | None = None
    """
    @staticmethod
    def _apply_filters(
            stmt: Select[tuple[OrmAppForm]],
            query: AppFormQuery,
    ) -> Select[tuple[OrmAppForm]]:
        clauses = []
        if query.user_id is not None:
            clauses.append(OrmAppForm.user_id == query.user_id)
        if query.country is not None:
            clauses.append(OrmAppForm.country == query.country)
        if query.country__in is not None:
            values = match_types(query.country__in, OrmAppForm.country)
            clauses.append(OrmAppForm.country.in_(values))
        if query.status is not None:
            clauses.append(OrmAppForm.status == query.status)
        if query.status__in is not None:
            values = match_types(query.status__in, OrmAppForm.status)
            clauses.append(OrmAppForm.status.in_(values))
        if query.status__not_in is not None:
            values = match_types(query.status__not_in, OrmAppForm.status)
            clauses.append(OrmAppForm.status.notin_(values))

        if len(clauses) > 0:
            stmt = stmt.where(and_(*clauses))
        """
        if query.search is not None:
            stmt = apply_search(stmt, query.search, VISA_SEARCH_BY)
        """
        return stmt


    async def get_many(self, query: AppFormQueryPaged) -> QueryResult[AppForm]:
        stmt = select(OrmAppForm)
        stmt = self._apply_filters(stmt, query)

        async with self.db.get_session() as session:
            total_items = await get_row_count(session, stmt)

            if query.sort_by is not None:
                stmt = apply_sorting(stmt, query.sort_by, query.sort)

            items, page, per_page, total_pages = [], None, None, None

            if query.page > 0 and query.per_page > 0 and total_items > 0:
                stmt = apply_pagination(stmt, query.page, query.per_page)
                orm_items = (await session.scalars(stmt)).all()
                items = TypeAdapter(list[AppForm]).validate_python(orm_items)

                page = query.page
                per_page = query.per_page
                total_pages = ceil(total_items / query.per_page)

            return QueryResult[AppForm](items=items,
                                     page=page,
                                     per_page=per_page,
                                     total_pages=total_pages,
                                     total_items=total_items)


    async def get_count(self, query: AppFormQuery) -> int:
        stmt = select(OrmAppForm)
        stmt = self._apply_filters(stmt, query)
        async with self.db.get_session() as session:
            return await get_row_count(session, stmt)


    async def get_count_by_status(self, query: AppFormQuery) -> list[QueryCountItem[AppFormStatus]]:
        column = OrmAppForm.status
        stmt = select(column, func.count(column))
        query.status = None
        query.status__in = None
        stmt = self._apply_filters(stmt, query)
        stmt = stmt.group_by(column).order_by(column)
        async with self.db.get_session() as session:
            result = (await session.execute(stmt)).all()
            return [QueryCountItem[AppFormStatus](value=item[0],
                                                  count=item[1]) for item in result]

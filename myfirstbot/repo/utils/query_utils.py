from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement, Select, and_, desc, func, null, or_ as _or_, select
from sqlalchemy.ext.asyncio import AsyncSession

import myfirstbot.entities.query.filters as _filters
import myfirstbot.entities.query.sorting as _sorting
from myfirstbot.entities.query.pagination import Pagination


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def single_clause(query: Select[Any], filter_: _filters.QueryFilter) -> ColumnElement[bool]:
    column: ColumnElement = query.selected_columns.get(filter_.field)
    error_msg = "Unknown filter type"
    match filter_.type:
        case _filters.EQ:
            clause = (column == filter_.value)
        case _filters.NE:
            clause = (column != filter_.value)
        case _filters.GT:
            clause = (column > filter_.value)
        case _filters.LT:
            clause = (column < filter_.value)
        case _filters.GE:
            clause = (column >= filter_.value)
        case _filters.LE:
            clause = (column <= filter_.value)
        case _filters.IN:
            clause = (column.in_(list(map(column.type.python_type, filter_.value))))
        case _filters.NIN:
            clause = (column.notin_(list(map(column.type.python_type, filter_.value))))
        case _filters.LIKE:
            clause = (column.ilike(f"%{esc_spec_chars(filter_.value)}%"))
        case _filters.IS:
            value = filter_.value if hasattr(filter_, "value") else null()
            clause = (column == value)
        case _filters.ISN:
            value = filter_.value if hasattr(filter_, "value") else null()
            clause = (column != value)
        case _:
            raise TypeError(error_msg)
    return clause


def multiple_clause(
        query: Select[Any], filters: Sequence[_filters.QueryFilter], *, or_: bool = False,
) -> ColumnElement[bool]:
    clauses = [single_clause(query, f) for f in filters]
    if or_:
        return _or_(*clauses)
    return and_(*clauses)


def apply_filter(query: Select[Any], filter_: _filters.QueryFilter) -> Select[Any]:
    return query.where(single_clause(query, filter_))


def apply_filters(
        query: Select[Any], filters: Sequence[_filters.QueryFilter], *, or_: bool = False,
) -> Select[Any]:
    return query.where(multiple_clause(query, filters, or_=or_))


def apply_sorting(query: Select[Any], sorting: _sorting.Sorting) -> Select[Any]:
    column: ColumnElement = query.selected_columns.get(sorting.order_by)
    if sorting.sort == _sorting.DESC:
        return query.order_by(desc(column))
    return query.order_by(column)


def apply_pagination(query: Select[Any], pagination: Pagination) -> Select[Any]:
    skip = (pagination.page - 1) * pagination.per_page
    return query.offset(skip).limit(pagination.per_page)


async def row_count(session: AsyncSession, query: Select[Any]) -> int:
    count_query = select(func.count()).select_from(query.subquery())
    return (await session.execute(count_query)).scalar_one()

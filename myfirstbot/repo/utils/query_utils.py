from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement, Select, and_, desc, func, null, or_ as _or_, select
from sqlalchemy.ext.asyncio import AsyncSession

import myfirstbot.entities.query.filters as _filters
import myfirstbot.entities.query.sorting as _sorting
from myfirstbot.entities.query import Pagination, Search


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def single_clause(query: Select[Any], filter_: _filters.QueryFilter) -> ColumnElement[bool]:  # noqa: PLR0911
    columns: dict[str, ColumnElement] = {}
    from_clauses = query.get_final_froms()
    for from_clause in from_clauses:
        columns |= from_clause.columns
    column = columns[filter_.field]

    value = filter_.value if filter_.value is not None else null()

    match filter_.type:
        case _filters.EQ:
            return column == value
        case _filters.NE:
            return column != value
        case _filters.GT:
            return column > value
        case _filters.LT:
            return column < value
        case _filters.GE:
            return column >= value
        case _filters.LE:
            return column <= value
        case _filters.IN:
            if hasattr(value, "__iter__"):
                return column.in_(list(map(column.type.python_type, value)))
        case _filters.NIN:
            if hasattr(value, "__iter__"):
                return column.notin_(list(map(column.type.python_type, value)))
        case _filters.LIKE:
            if isinstance(value, str):
                return column.ilike(f"%{esc_spec_chars(value)}%")
        case _filters.IS:
            value = null() if value is None else value
            return column == value
        case _filters.ISN:
            value = null() if value is None else value
            return column != value

    error_msg = "Unknown filter type"
    raise TypeError(error_msg)


def multiple_clause(
        query: Select[Any],
        filters: Sequence[_filters.QueryFilter],
        *,
        or_: bool = False,
) -> ColumnElement[bool]:
    clauses = [single_clause(query, f) for f in filters]
    if or_:
        return _or_(*clauses)
    return and_(*clauses)


def apply_filter(query: Select[Any], filter_: _filters.QueryFilter) -> Select[Any]:
    return query.where(single_clause(query, filter_))


def apply_filters(
        query: Select[Any],
        filters: Sequence[_filters.QueryFilter],
        *,
        or_: bool = False,
) -> Select[Any]:
    return query.where(multiple_clause(query, filters, or_=or_))


def apply_search(
        query: Select[Any],
        search: Search,
) -> Select[Any]:
    filters = [_filters.StrQueryFilter(field=field, type="like", value=search.s)
              for field in search.fields]
    return query.where(multiple_clause(query, filters, or_=True))


def apply_sorting(query: Select[Any], sorting: _sorting.Sorting) -> Select[Any]:
    column: ColumnElement = query.selected_columns[sorting.order_by]
    if sorting.sort == _sorting.DESC:
        return query.order_by(desc(column))
    return query.order_by(column)


def apply_pagination(query: Select[Any], pagination: Pagination) -> Select[Any]:
    skip = (pagination.page - 1) * pagination.per_page
    return query.offset(skip).limit(pagination.per_page)


async def get_count(session: AsyncSession, query: Select[Any]) -> int:
    count_query = select(func.count()).select_from(query.subquery())
    return (await session.execute(count_query)).scalar_one()


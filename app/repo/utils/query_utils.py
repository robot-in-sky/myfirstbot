from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement, Select, and_, desc, func, null, or_ as _or_, select
from sqlalchemy.ext.asyncio import AsyncSession

import app.entities.query.filters as _filters
import app.entities.query.sorting as _sorting
from app.entities.query import Pagination, Search


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def single_clause(stmt: Select[Any], filter_: _filters.QueryFilter) -> ColumnElement[bool]:  # noqa: PLR0911
    columns: dict[str, ColumnElement[Any]] = {}
    from_clauses = stmt.get_final_froms()
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
        stmt: Select[Any],
        filters: Sequence[_filters.QueryFilter],
        *,
        or_: bool = False,
) -> ColumnElement[bool]:
    clauses = [single_clause(stmt, f) for f in filters]
    if or_:
        return _or_(*clauses)
    return and_(*clauses)


def apply_filter(stmt: Select[Any], filter_: _filters.QueryFilter) -> Select[Any]:
    return stmt.where(single_clause(stmt, filter_))


def apply_filters(
        stmt: Select[Any],
        filters: Sequence[_filters.QueryFilter],
        *,
        or_: bool = False,
) -> Select[Any]:
    return stmt.where(multiple_clause(stmt, filters, or_=or_))


def apply_search(
        stmt: Select[Any],
        search: Search,
) -> Select[Any]:
    filters = [_filters.StrQueryFilter(field=field, type="like", value=search.s)
              for field in search.fields]
    return stmt.where(multiple_clause(stmt, filters, or_=True))


def apply_sorting(stmt: Select[Any], sorting: _sorting.Sorting) -> Select[Any]:
    column: ColumnElement[Any] = stmt.selected_columns[sorting.order_by]
    if sorting.sort == _sorting.DESC:
        return stmt.order_by(desc(column))
    return stmt.order_by(column)


def apply_pagination(stmt: Select[Any], pagination: Pagination) -> Select[Any]:
    skip = (pagination.page - 1) * pagination.per_page
    return stmt.offset(skip).limit(pagination.per_page)


async def get_count(session: AsyncSession, stmt: Select[Any]) -> int:
    count_stmt = select(func.count()).select_from(stmt.subquery())
    return (await session.execute(count_stmt)).scalar_one()

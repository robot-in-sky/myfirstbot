from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement, Select, and_, desc, null, or_ as _or_

import myfirstbot.base.entities.query as _query


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def single_clause(query: Select[Any], filter_: _query.QueryFilter) -> ColumnElement[bool]:
    column: ColumnElement = query.selected_columns.get(filter_.field)
    error_msg = "Unknown filter type"
    match filter_.type:
        case _query.EQ:
            clause = (column == filter_.value)
        case _query.NE:
            clause = (column != filter_.value)
        case _query.GT:
            clause = (column > filter_.value)
        case _query.LT:
            clause = (column < filter_.value)
        case _query.GE:
            clause = (column >= filter_.value)
        case _query.LE:
            clause = (column <= filter_.value)
        case _query.IN:
            clause = (column.in_(list(map(column.type.python_type, filter_.value))))
        case _query.NIN:
            clause = (column.notin_(list(map(column.type.python_type, filter_.value))))
        case _query.LIKE:
            clause = (column.ilike(f"%{esc_spec_chars(filter_.value)}%"))
        case _query.IS:
            value = filter_.value if hasattr(filter_, "value") else null()
            clause = (column == value)
        case _query.ISN:
            value = filter_.value if hasattr(filter_, "value") else null()
            clause = (column != value)
        case _:
            raise TypeError(error_msg)
    return clause


def multiple_clause(
        query: Select[Any], filters: Sequence[_query.QueryFilter], *, or_: bool = False,
) -> ColumnElement[bool]:
    clauses = [single_clause(query, f) for f in filters]
    if or_:
        return _or_(*clauses)
    return and_(*clauses)


def apply_filter(query: Select[Any], filter_: _query.QueryFilter) -> Select[Any]:
    return query.where(single_clause(query, filter_))


def apply_filters(
        query: Select[Any], filters: Sequence[_query.QueryFilter], *, or_: bool = False,
) -> Select[Any]:
    return query.where(multiple_clause(query, filters, or_=or_))


def apply_sorting(query: Select[Any], sorting: _query.Sorting) -> Select[Any]:
    column: ColumnElement = query.selected_columns.get(sorting.order_by)
    if sorting.sort == _query.DESC:
        return query.order_by(desc(column))
    return query.order_by(column)


def apply_pagination(query: Select[Any], pagination: _query.Pagination) -> Select[Any]:
    skip = (pagination.page - 1) * pagination.page_size
    return query.offset(skip).limit(pagination.page_size)

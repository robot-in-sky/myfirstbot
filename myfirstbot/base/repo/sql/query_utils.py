from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement, Select, and_, desc, null, or_

import myfirstbot.base.entities.query as _query


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def single_clause(query: Select[Any], filter_: _query.QueryFilter) -> ColumnElement[bool]:
    column: ColumnElement = query.selected_columns.get(filter_.field)
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
        case _query.ISN:
            clause = (column == null())
        case _query.ISNN:
            clause = (column != null())
        case _:
            message = "Unknown filter type"
            raise TypeError(message)
    return clause


def group_clause(query: Select[Any], filter_group: _query.FilterGroup) -> ColumnElement[bool]:
    clause = None
    for item in filter_group.filters:
        if isinstance(item, _query.QueryFilter):
            if clause is None:
                clause = single_clause(query, item)
            elif filter_group.join_type == _query.OR:
                clause = or_(clause, single_clause(query, item))
            else:
                clause = and_(clause, single_clause(query, item))

        if isinstance(item, _query.FilterGroup):
            clause = group_clause(query, item)

    return clause


def apply_filter(query: Select[Any], filter_: _query.QueryFilter) -> Select[Any]:
    return query.where(single_clause(query, filter_))


def apply_filters(
        query: Select[Any],
        filters: Sequence[_query.QueryFilter] | _query.FilterGroup,
) -> Select[Any]:
    if not isinstance(filters, _query.FilterGroup):
        filters = _query.FilterGroup(filters=filters)
    return query.where(group_clause(query, filters))


def apply_sorting(query: Select[Any], sorting: _query.Sorting) -> Select[Any]:
    column: ColumnElement = query.selected_columns.get(sorting.order_by)
    if sorting.sort == _query.DESC:
        return query.order_by(desc(column))
    return query.order_by(column)


def apply_pagination(query: Select[Any], pagination: _query.Pagination) -> Select[Any]:
    skip = (pagination.page - 1) * pagination.page_size
    return query.offset(skip).limit(pagination.page_size)

from collections.abc import Iterable
from typing import Any

from sqlalchemy import ColumnElement, Select, and_, or_

import myfirstbot.base.entities.filters as _filters


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def single_clause(query: Select[Any], filter_: _filters.QueryFilter) -> ColumnElement:
    column_el: ColumnElement = query.selected_columns.get(filter_.field)
    match filter_.type:
        case _filters.EQ:
            clause = (column_el == filter_.value)
        case _filters.NE:
            clause = (column_el != filter_.value)
        case _filters.GT:
            clause = (column_el > filter_.value)
        case _filters.LT:
            clause = (column_el < filter_.value)
        case _filters.GE:
            clause = (column_el >= filter_.value)
        case _filters.LE:
            clause = (column_el <= filter_.value)
        case _filters.IN:
            clause = (column_el.in_(list(map(column_el.type.python_type, filter_.value))))
        case _filters.NIN:
            clause = (column_el.notin_(list(map(column_el.type.python_type, filter_.value))))
        case _filters.LIKE:
            clause = (column_el.ilike(f"%{esc_spec_chars(filter_.value)}%"))
        case _:
            message = "Unknown filter type"
            raise TypeError(message)
    return clause

def group_clause(
        query: Select[Any], filter_group: _filters.QueryFilterGroup
) -> ColumnElement:
    clause = None
    for item in filter_group:
        if isinstance(item, _filters.QueryFilter):
            if clause:
                if filter_group.join_type == _filters.OR:
                    clause = or_(clause, single_clause(query, item))
                else:
                    clause = and_(clause, single_clause(query, item))
            else:
                clause = single_clause(query, item)

        if isinstance(item, _filters.QueryFilterGroup):
            clause = group_clause(query, item)

    return clause


def apply_filter(query: Select[Any], filter_: _filters.QueryFilter) -> Select[Any]:
    return query.where(single_clause(query, filter_))

def apply_filters(query: Select[Any], filters: _filters.QueryFilterGroup) -> Select[Any]:
    return query.where(group_clause(query, filters))




# def apply_pagination(query: Select[Any], page: int, page_size: int) -> Select[Any]:

# def apply_sorting(query: Select[Any],) -> Select[Any]:

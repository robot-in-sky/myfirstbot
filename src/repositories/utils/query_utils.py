from collections.abc import Collection
from typing import Any

from sqlalchemy import ColumnElement, Select, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


def get_column(stmt: Select[Any], name: str) -> ColumnElement[Any] | None:
    return stmt.selected_columns.get(name)


def match_types(values: Collection[Any], column: ColumnElement[Any]) -> list[Any]:
    return list(map(column.type.python_type, values))


def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])


def apply_search(
        stmt: Select[Any],
        search: str,
        search_in_columns: Collection[str],
) -> Select[Any]:
    clauses = []
    for name in search_in_columns:
        column = get_column(stmt, name)
        if column is not None:
            search = esc_spec_chars(search)
            clause = column.like(f"%{search}%")
            clauses.append(clause)
    if len(clauses) == 0:
        return stmt
    return stmt.where(or_(*clauses))


def apply_sorting(stmt: Select[Any], sort_by: str, sort: str | None) -> Select[Any]:
    column = get_column(stmt, sort_by)
    if column is None:
        return stmt
    if sort == "desc":
        return stmt.order_by(desc(column))
    return stmt.order_by(column)


def apply_pagination(stmt: Select[Any], page: int, per_page: int) -> Select[Any]:
    skip = (page - 1) * per_page
    return stmt.offset(skip).limit(per_page)


async def get_row_count(session: AsyncSession, stmt: Select[Any]) -> int:
    count_stmt = select(func.count()).select_from(stmt.subquery())
    return (await session.execute(count_stmt)).scalar_one()

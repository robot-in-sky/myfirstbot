from __future__ import annotations

from collections.abc import Sequence  # noqa: TCH003
from typing import Literal

from pydantic import BaseModel, PositiveInt

""" Filter types """
EQ = "eq"  # equal
NE = "ne"  # not equal
GT = "gt"  # greater than
LT = "lt"  # less than
GE = "ge"  # greater than or equal
LE = "le"  # less than or equal
IN = "in"  # in
NIN = "nin"  # not in
LIKE = "like"  # like
ISN = "isn"  # is null
ISNN = "isnn"  # is not null

""" Filter join types """
AND = "and"
OR = "or"

""" Sorting types """
ASC = "and"
DESC = "or"


class NumQueryFilter(BaseModel):
    type: Literal["eq", "ne", "gt", "lt", "ge", "le"] = "eq"
    field: str
    value: int | float


class StrQueryFilter(BaseModel):
    type: Literal["eq", "ne", "like"] = "eq"
    field: str
    value: str


class NullQueryFilter(BaseModel):
    type: Literal["isn", "isnn"] = "isn"
    field: str


class SetQueryFilter(BaseModel):
    type: Literal["in", "nin"] = "in"
    field: str
    value: set[str | int]


class AgeQueryFilter(BaseModel):
    type: Literal["gt", "lt", "ge", "le"]
    field: str
    value: int


QueryFilter = NumQueryFilter | StrQueryFilter | NullQueryFilter | SetQueryFilter | AgeQueryFilter


class FilterGroup(BaseModel):
    filters: Sequence[QueryFilter] | FilterGroup
    join_type: Literal["and", "or"] = "and"


class Sorting(BaseModel):
    order_by: str
    sort: Literal["asc", "desc"] = "asc"


class Pagination(BaseModel):
    page: PositiveInt = 1
    page_size: PositiveInt = 10

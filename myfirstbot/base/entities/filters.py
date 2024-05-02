from collections.abc import Iterable
from typing import Literal, Self

from pydantic import BaseModel

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

""" Join types """
AND = "and"
OR = "or"


class NumQueryFilter(BaseModel):
    type: Literal["eq", "ne", "gt", "lt", "ge", "le"] = "eq"
    field: str
    value: int | float


class StrQueryFilter(BaseModel):
    type: Literal["eq", "ne", "like"] = "eq"
    field: str
    value: str


class SetQueryFilter(BaseModel):
    type: Literal["in", "nin"] = "in"
    field: str
    value: set[str | int]


class AgeQueryFilter(BaseModel):
    type: Literal["gt", "lt", "ge", "le"]
    field: str
    value: int


QueryFilter = NumQueryFilter | StrQueryFilter | SetQueryFilter | AgeQueryFilter


class QueryFilterGroup(BaseModel):
    filters: Iterable[QueryFilter | Self]
    join_type: Literal["and", "or"] = "and"

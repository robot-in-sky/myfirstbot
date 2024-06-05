from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel

""" Filter types """
EQ = "eq"  # equal
NE = "ne"  # not equal
GT = "gt"  # greater than
LT = "lt"  # less than
GE = "ge"  # greater than or equal
LE = "le"  # less than or equal
LIKE = "like"  # like
IS = "is"  # is
ISN = "isn"  # is not
IN = "in"  # in
NIN = "nin"  # not in


class NumQueryFilter(BaseModel):
    field: str
    type: Literal["eq", "ne", "gt", "lt", "ge", "le"] = "eq"
    value: int | float


class StrQueryFilter(BaseModel):
    field: str
    type: Literal["eq", "ne", "like"] = "eq"
    value: str


class ChoiceQueryFilter(BaseModel):
    field: str
    type: Literal["is", "isn"] = "is"
    value: Enum


class DateTimeQueryFilter(BaseModel):
    field: str
    type: Literal["gt", "lt"]
    value: datetime


class IsNullQueryFilter(BaseModel):
    field: str
    type: Literal["is", "isn"] = "isn"


class InSetQueryFilter(BaseModel):
    field: str
    type: Literal["in", "nin"] = "in"
    value: set[str | int | Enum]


QueryFilter = (NumQueryFilter | StrQueryFilter | ChoiceQueryFilter
               | DateTimeQueryFilter | IsNullQueryFilter | InSetQueryFilter)

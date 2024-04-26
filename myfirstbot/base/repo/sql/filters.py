from operator import or_
from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy import Interval, Select, cast, func, text

from myfirstbot.base.entities import Filter, _FilterFieldT
from myfirstbot.base.entities.enums.filter_type import FilterType
from myfirstbot.base.utils.helpers import esc_spec_chars

if TYPE_CHECKING:
    from sqlalchemy.orm import InstrumentedAttribute

_OrmModelT = TypeVar("_OrmModelT")


class QueryFilter:
    def __new__(cls, filter_: Filter[_FilterFieldT], orm_model: type[_OrmModelT]) -> "QueryFilter":
        for subclass in cls.__subclasses__():
            if subclass.type == filter_.type:
                instance = object.__new__(subclass)
                instance.__init__(filter_=filter_, orm_model=orm_model)  # type: ignore[misc]
                return instance

        error_message = f"Unsupported filter type: {filter_.type}"
        raise ValueError(error_message)

    def __init__(self, filter_: Filter[_FilterFieldT], orm_model: type[_OrmModelT]) -> None:
        self.filter = filter_
        self.filter_column: InstrumentedAttribute[Any] | None = (
            getattr(orm_model, filter_.field) if filter_.field else None
        )

    @property
    def type(self) -> FilterType:
        raise NotImplementedError

    def apply(self, query: Select[Any]) -> Select[Any]:
        raise NotImplementedError


class EQQueryFilter(QueryFilter):
    type = FilterType.EQ

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(self.filter_column == self.filter.value)


class GEQueryFilter(QueryFilter):
    type = FilterType.GE

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(self.filter_column >= self.filter.value)


class LEQueryFilter(QueryFilter):
    type = FilterType.LE

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(self.filter_column <= self.filter.value)


class LikeQueryFilter(QueryFilter):
    type = FilterType.LIKE

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(self.filter_column.ilike(f"%{esc_spec_chars(self.filter.value)}%"))


class INQueryFilter(QueryFilter):
    type = FilterType.IN

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(
            self.filter_column.in_([self.filter_column.type.python_type(value) for value in self.filter.value]),
        )


class AGEQueryFilter(QueryFilter):
    type = FilterType.AGE

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(
            or_(
                self.filter_column.is_(None),
                (func.now() - self.filter_column) >= cast(text(f"'{self.filter.value} seconds'"), Interval),
            ),
        )


class RAWQueryFilter(QueryFilter):
    type = FilterType.RAW

    def apply(self, query: Select[Any]) -> Select[Any]:
        return query.where(text(self.filter.value))

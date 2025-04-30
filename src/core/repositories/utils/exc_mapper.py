from collections.abc import Callable
from functools import wraps
from typing import Any

from psycopg.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    ForeignKeyViolationError,
    UniqueViolationError,
)


def exception_mapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except IntegrityError as error:
            if isinstance(error.orig, ForeignKeyViolation):
                raise ForeignKeyViolationError from error
            if isinstance(error.orig, UniqueViolation):
                raise UniqueViolationError from error
            raise
    return wrapped


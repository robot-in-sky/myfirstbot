from collections.abc import Callable
from functools import wraps
from typing import Any

from sqlalchemy.exc import DBAPIError

from myfirstbot.exceptions import (
    ForeignKeyViolationError,
    UniqueViolationError,
)


def exception_mapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any) -> None:
        try:
            return await func(*args, **kwargs)
        except DBAPIError as error:
            if hasattr(error.orig, "pgcode"):
                if error.orig.pgcode == "23503":
                    raise ForeignKeyViolationError from error
                if error.orig.pgcode == "23505":
                    raise UniqueViolationError from error
            raise
    return wrapped


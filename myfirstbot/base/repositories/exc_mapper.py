from collections.abc import Callable
from functools import wraps
from typing import Any

from asyncpg.exceptions import (
    ForeignKeyViolationError as _ForeignKeyViolationError,
    UniqueViolationError as _UniqueViolationError,
)
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from myfirstbot.db.exceptions import ForeignKeyViolationError, SchemaValidationError, UniqueViolationError


def exception_mapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any):
        try:
            return await func(*args, **kwargs)
        except ValidationError as error:
            raise SchemaValidationError from error
        except IntegrityError as error:
            if isinstance(error.orig.__cause__, _UniqueViolationError):
                raise UniqueViolationError from error
            elif isinstance(error.orig.__cause__, _ForeignKeyViolationError):
                raise ForeignKeyViolationError from error
            raise

    return wrapped


from collections.abc import Callable
from functools import wraps
from typing import Any

# from asyncpg.exceptions import (
#     ForeignKeyViolationError as _ForeignKeyViolationError,
#     NotNullViolationError as _NotNullViolationError,
#     UniqueViolationError as _UniqueViolationError,
# )
# from psycopg.errors import (
#     ForeignKeyViolation as _ForeignKeyViolationError,
#     NotNullViolation as _NotNullViolationError,
#     UniqueViolation as _UniqueViolationError,
# )
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError

from myfirstbot.exceptions import (
    ForeignKeyViolationError,
    NotNullViolationError,
    SchemaValidationError,
    UniqueViolationError,
)


def exception_mapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any) -> None:
        try:
            return await func(*args, **kwargs)
        except ValidationError as error:
            raise SchemaValidationError from error
        except DBAPIError as error:
            if hasattr(error.orig, "pgcode"):
                if error.orig.pgcode == "23502":
                    raise NotNullViolationError from error
                if error.orig.pgcode == "23503":
                    raise ForeignKeyViolationError from error
                if error.orig.pgcode == "23505":
                    raise UniqueViolationError from error
            # if isinstance(error.orig.__cause__, _ForeignKeyViolationError):
            #     raise ForeignKeyViolationError from error
            # if isinstance(error.orig.__cause__, _NotNullViolationError):
            #     raise NotNullViolationError from error
            # if isinstance(error.orig.__cause__, _UniqueViolationError):
            #     raise UniqueViolationError from error
            raise

    return wrapped


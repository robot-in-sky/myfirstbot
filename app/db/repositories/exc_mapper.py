from functools import wraps
from typing import Any, Callable

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from asyncpg.exceptions import \
    UniqueViolationError as _UniqueViolationError, \
    ForeignKeyViolationError as _ForeignKeyViolationError

from app.db.exceptions import \
    UniqueViolationError, ForeignKeyViolationError, SchemaValidationError


def exception_mapper(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any):
        try:
            return await func(*args, **kwargs)
        except ValidationError:
            raise SchemaValidationError()
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, _UniqueViolationError):
                raise UniqueViolationError()
            elif isinstance(e.orig.__cause__, _ForeignKeyViolationError):
                raise ForeignKeyViolationError()
            pass

    return wrapped


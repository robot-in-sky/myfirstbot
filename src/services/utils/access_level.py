from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any

from src.entities.users import UserRole
from src.exceptions import AccessDeniedError

if TYPE_CHECKING:
    from src.entities.users.user import User


def access_level(required: UserRole) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            current_user: User = args[0].current_user
            if current_user.role < required:
                raise AccessDeniedError
            return await func(*args, **kwargs)
        return wrapped
    return decorator

from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any

from app.entities.choices.user_role import UserRole
from app.exceptions import AccessDeniedError

if TYPE_CHECKING:
    from app.entities.user import User


def access_level(required: UserRole) -> Callable:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> None:
            current_user: User = args[0].current_user
            if current_user.role < required:
                raise AccessDeniedError
            return await func(*args, **kwargs)
        return wrapped
    return decorator

from .commands import router as _commands
from .errors import router as _errors
from .order import router as _orders
from .user import router as _users

routers = (
    _commands,
    _errors,
    _orders,
    _users,
)

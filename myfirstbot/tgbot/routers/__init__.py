from .commands import router as _commands
from .order import router as _orders
from .user import router as _users

routers = (
    _commands,
    _orders,
    _users
)

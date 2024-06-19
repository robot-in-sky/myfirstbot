from .commands import router as _commands
from .orders import router as _orders
from .users import router as _users

routers = (
    _commands,
    _orders,
    _users
)

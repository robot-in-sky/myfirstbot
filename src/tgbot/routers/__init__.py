from .commands import router as _commands
from .errors import router as _errors
from .order import router as _orders
from .user import router as _users
from .visa_form import router as _visa_forms

routers = (
    _commands,
    _errors,
    _orders,
    _users,
    _visa_forms
)

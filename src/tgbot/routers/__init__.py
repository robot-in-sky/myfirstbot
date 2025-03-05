from .commands import router as _commands
from .errors import router as _errors
from .visa import router as _visas

routers = (
    _commands,
    _errors,
    _visas,
)

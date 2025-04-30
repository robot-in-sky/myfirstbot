from .base_router import router as _base_router
from .public_router import router as _public_router

routers = (
    _base_router,
    _public_router,
)

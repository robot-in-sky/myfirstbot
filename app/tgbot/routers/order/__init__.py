from aiogram import Router

from .order import router as _order
from .orders import router as _orders

child_routers = (
    _orders,
    _order,
)

router = Router()
router.include_routers(*child_routers)

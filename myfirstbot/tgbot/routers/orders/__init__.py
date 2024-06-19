from aiogram import Router

from .edit_order import router as _edit_order
from .new_order import router as _new_order
from .order import router as _order
from .orders import router as _orders

child_routers = (
    _new_order,
    _orders,
    _order,
    _edit_order,
)

router = Router()
router.include_routers(*child_routers)

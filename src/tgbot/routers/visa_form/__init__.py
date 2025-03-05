from aiogram import Router

from .visa_form import router as _order
from .visa_forms import router as _orders

child_routers = (
    _orders,
    _order,
)

router = Router()
router.include_routers(*child_routers)

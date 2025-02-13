from aiogram import Router

from .visa import router as _visa

child_routers = (
    _visa,
)

router = Router()
router.include_routers(*child_routers)

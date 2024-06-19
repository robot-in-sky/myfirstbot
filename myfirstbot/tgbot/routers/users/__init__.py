from aiogram import Router

from .user import router as _user
from .users import router as _users

child_routers = (
    _users,
    _user,
)

router = Router()
router.include_routers(*child_routers)

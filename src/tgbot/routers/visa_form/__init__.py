from aiogram import Router

from .visa_form import router as _visa_form
# from .visa_forms import router as _visa_forms

child_routers = (
    # _visa_forms,
    _visa_form,
)

router = Router()
router.include_routers(*child_routers)

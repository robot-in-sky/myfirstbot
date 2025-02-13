from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry

from src.tgbot.scenes.visa.fill_form import FillFormScene
from src.tgbot.scenes.visa.edit_section import EditSectionScene
from src.tgbot.scenes.visa.apply_visa import ApplyVisaScene
from src.tgbot.views import buttons

router = Router()
scene_registry = SceneRegistry(router)
scene_registry.add(ApplyVisaScene)
scene_registry.add(FillFormScene)
scene_registry.add(EditSectionScene)

router.message.register(
    ApplyVisaScene.as_handler(), F.text == buttons.NEW_ORDER)
router.callback_query.register(
    ApplyVisaScene.as_handler(), F.data == "fill_visa_form")

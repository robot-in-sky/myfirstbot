from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry

from src.tgbot.scenes.public.my_app_forms import MyAppFormsScene
from src.tgbot.scenes.visa.apply_visa import ApplyVisaScene
from src.tgbot.scenes.visa.form import FormScene
from src.tgbot.scenes.visa.repeater import RepeaterScene
from src.tgbot.scenes.visa.section import SectionScene
from src.tgbot.views import buttons

router = Router()
scene_registry = SceneRegistry(router)
scene_registry.add(MyAppFormsScene)
scene_registry.add(ApplyVisaScene)
scene_registry.add(FormScene)
scene_registry.add(SectionScene)
scene_registry.add(RepeaterScene)

router.message.register(
    MyAppFormsScene.as_handler(), F.text == buttons.MY_APP_FORMS)
router.callback_query.register(
    MyAppFormsScene.as_handler(), F.data == "my_app_forms")

router.message.register(
    ApplyVisaScene.as_handler(), F.text == buttons.APPLY_VISA)
router.callback_query.register(
    ApplyVisaScene.as_handler(), F.data == "apply_visa")

from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry

from interfaces.tgbot.scenes.public.apply_visa_scene import ApplyVisaScene
from interfaces.tgbot.scenes.public.before_apply_scene import BeforeApplyScene
from interfaces.tgbot.scenes.public.my_app_form_scene import MyAppFormScene
from interfaces.tgbot.scenes.public.my_app_forms_scene import MyAppFormsScene
from interfaces.tgbot.scenes.public.survey_repeater_scene import SurveyRepeaterScene
from interfaces.tgbot.scenes.public.survey_scene import SurveyScene
from interfaces.tgbot.scenes.public.survey_section_scene import SurveySectionScene
from interfaces.tgbot.views import buttons

router = Router()
scene_registry = SceneRegistry(router)
scene_registry.add(BeforeApplyScene)
scene_registry.add(ApplyVisaScene)
scene_registry.add(SurveyScene)
scene_registry.add(SurveySectionScene)
scene_registry.add(SurveyRepeaterScene)
scene_registry.add(MyAppFormsScene)
scene_registry.add(MyAppFormScene)

router.message.register(
    MyAppFormsScene.as_handler(), F.text == buttons.MY_APP_FORMS)
router.callback_query.register(
    MyAppFormsScene.as_handler(), F.data == "my_app_forms")

router.message.register(
    BeforeApplyScene.as_handler(), F.text == buttons.APPLY_VISA)
router.callback_query.register(
    BeforeApplyScene.as_handler(), F.data == "apply_visa")

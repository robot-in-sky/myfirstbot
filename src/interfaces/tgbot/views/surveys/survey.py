from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from interfaces.tgbot.views import buttons

SURVEY_DONE_TEXT = ("🎉🎉🎉 <b>Ура! Анкета заполнена!</b>\n"
                  "Сохраняем данные?")
SURVEY_RECHECK_TEXT = "📝 Проверяем всё с начала"

def survey_check_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons.FORM_RECHECK, callback_data="survey:recheck")],
        [InlineKeyboardButton(text=buttons.SAVE, callback_data="survey:save")]])


async def show_survey_done_message(message: Message) -> Message:
    text = SURVEY_DONE_TEXT
    keyboard = survey_check_kb()
    return await message.answer(text, reply_markup=keyboard)

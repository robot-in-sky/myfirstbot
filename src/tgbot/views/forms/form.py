from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.tgbot.views import buttons

FORM_DONE_TEXT = ("🎉🎉🎉 <b>Ура! Анкета заполнена!</b>\n"
                  "Сохраняем данные?")
FORM_RECHECK_TEXT = "📝 Проверяем всё с начала"

def form_check_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons.FORM_RECHECK, callback_data="form:recheck")],
        [InlineKeyboardButton(text=buttons.SAVE, callback_data="form:save")]])


async def show_form_done_message(message: Message) -> Message:
    text = FORM_DONE_TEXT
    keyboard = form_check_kb()
    return await message.answer(text, reply_markup=keyboard)

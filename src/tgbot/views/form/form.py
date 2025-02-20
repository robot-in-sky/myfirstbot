from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.tgbot.views import buttons

FORM_DONE_TEXT = ("🎉🎉🎉 Ура! Анкета заполнена!\n"
                  "Сохраняем данные?")
FORM_RECHECK = "⏫ Начнём с начала"

def form_check_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=buttons.CHECK_AGAIN, callback_data="form:recheck")],
        [InlineKeyboardButton(text=buttons.SAVE, callback_data="form:save")]])


async def show_form_done_message(message: Message) -> Message:
    text = FORM_DONE_TEXT
    keyboard = form_check_kb()
    return await message.answer(text, reply_markup=keyboard)

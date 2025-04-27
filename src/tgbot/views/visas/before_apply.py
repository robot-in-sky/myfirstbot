from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

USE_DRAFT_STEP_TEXT = ("<b>У Вас есть незавершённые анкеты</b>\n\n"
                       "Продолжить заполнение существующей анкеты?")

USE_COMPLETED_STEP_TEXT = ("<b>У Вас есть завершённые анкеты</b>\n\n"
                           "Хотите использовать имеющиеся данные для создания новой анкеты?")


async def show_use_saved_step(message: Message) -> None:
    await message.edit_text(USE_DRAFT_STEP_TEXT, reply_markup=step_kb())


async def show_use_completed_step(message: Message) -> None:
    await message.edit_text(USE_COMPLETED_STEP_TEXT, reply_markup=step_kb())


def step_kb() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text="Да", callback_data="yes"),
                 InlineKeyboardButton(text="Нет, всё сначала", callback_data="no")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

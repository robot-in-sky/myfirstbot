from aiogram.types import Message, ReplyKeyboardRemove

SECTION_DONE_TEXTS = ["Проверьте введённые данные",
                      "Отлично! Проверьте данные",
                      "А теперь проверьте"]


def get_section_done_text(step: int) -> str:
    idx = step % len(SECTION_DONE_TEXTS)
    return SECTION_DONE_TEXTS[idx]


async def show_section_done_message(message: Message, *, step: int) -> None:
    text = get_section_done_text(step)
    await message.answer(text, reply_markup=ReplyKeyboardRemove())

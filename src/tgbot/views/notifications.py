from aiogram.types import Message


async def show_notice(notice: str, *, message: Message, replace: bool = False) -> Message:
    text = f"<i>{notice}</i>"
    if replace:
        await message.edit_text(text)
        return message
    return await message.answer(text)

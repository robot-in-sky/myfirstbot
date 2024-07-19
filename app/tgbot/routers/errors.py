import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, ErrorEvent, Message

router = Router()


@router.error()
async def error_handler(event: ErrorEvent) -> None:
    if event.update.callback_query:
        await event.update.callback_query.answer()
        username = event.update.callback_query.from_user.username
        message = event.update.callback_query.message
    else:
        username = event.update.message.from_user.username
        message = event.update.message
    if isinstance(message, Message):
        await message.answer("💁‍♂️ Упс... Что-то пошло не так")
        logging.critical(f"{type(event.exception)} [@{username}]: {event.exception}")


@router.callback_query(F.data == "_")
async def do_nothing_callback_handler(query: CallbackQuery) -> None:
    await query.answer()
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router(name="help")


@help_router.message(Command(commands="help"))
async def help_handler(message: types.Message) -> Message:
    return await message.answer("Hi, world!")

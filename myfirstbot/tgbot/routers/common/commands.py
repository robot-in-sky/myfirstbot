from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from myfirstbot.entities.user import User
from myfirstbot.tgbot.views.common.main_menu import main_menu_kb

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, user: User) -> None:
    await message.answer(
        f"Приветствую, {user.user_name}!\n"
        "Я — тестовый бот-пример для управления заказами",
        reply_markup=main_menu_kb(user),
    )

@router.message(Command(commands="menu"))
async def command_menu_handler(message: Message, user: User) -> None:
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb(user),
    )

@router.message(Command(commands="help"))
async def help_handler(message: types.Message) -> Message:
    return await message.answer("Hi, world!")
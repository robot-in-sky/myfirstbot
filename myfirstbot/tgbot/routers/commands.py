from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import ScenesManager
from aiogram.types import CallbackQuery, Message, ErrorEvent

from myfirstbot.entities.user import User
from myfirstbot.exceptions import ValidationError
from myfirstbot.tgbot.views.menu import main_menu_kb

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, user: User, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        f"Приветствую, {user.user_name}!\n"
        "Я — тестовый бот-пример для управления заказами",
        reply_markup=main_menu_kb(user),
    )


@router.message(Command(commands="menu"))
async def command_menu_handler(message: Message, user: User, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb(user),
    )


@router.message(Command(commands="help"))
async def help_handler(message: types.Message, state: FSMContext) -> Message:
    await state.clear()
    return await message.answer("Hi, world!")


@router.callback_query(F.data == "_")
async def do_nothing_callback(query: CallbackQuery) -> None:
    await query.answer()


@router.error(ExceptionTypeFilter(ValidationError), F.update.message.as_("message"))
async def handle_validation_error(event: ErrorEvent, message: Message) -> None:
    await message.answer(str(event.exception))

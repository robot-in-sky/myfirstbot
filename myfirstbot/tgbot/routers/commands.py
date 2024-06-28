from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent, Message

from myfirstbot.entities.user import User
from myfirstbot.exceptions import InvalidStateError, ValidationError
from myfirstbot.tgbot.views.menu import main_menu_kb

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, current_user: User, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Приветствую, <b>{current_user.user_name}</b>!\n"
                         "Я — тестовый бот-пример для управления заказами",
                         reply_markup=main_menu_kb(current_user))


@router.message(Command(commands="menu"))
async def command_menu_handler(message: Message, current_user: User, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Главное меню",
                         reply_markup=main_menu_kb(current_user))


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


@router.error(ExceptionTypeFilter(InvalidStateError), F.update.message.as_("message"))
async def handle_invalid_state_error(message: Message) -> None:
    await message.answer("Невозможно выполнить действие")

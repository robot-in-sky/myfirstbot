from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent, Message

from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AccessDeniedError, InvalidStateError, ValidationError
from myfirstbot.repo.utils import Database
from myfirstbot.services import UserService
from myfirstbot.tgbot.views.menu import show_menu, signin_menu_kb
from myfirstbot.tgbot.views.user.user import user_role

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, current_user: User, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Приветствую, <b>{current_user.user_name}</b>!\n"
                         "Это тестовая версия бота для управления заказами.\n\n"
                         "<b>Пользователи</b> могут создавать заказы (заявки/запросы/анкеты).\n"
                         "<b>Агенты/менеджеры</b> обрабатывают поступающие заказы.\n\n"
                         "В качестве кого вы хотите продолжить?",
                         reply_markup=signin_menu_kb())


@router.callback_query(F.data.startswith("signin_as:"))
async def signin_as_callback(query: CallbackQuery, db: Database, current_user: User) -> None:
    service = UserService(db, current_user)
    match query.data:
        case "signin_as:agent":
            await service.set_role(current_user.id, UserRole.AGENT)
        case "signin_as:user" | _:
            await service.set_role(current_user.id, UserRole.USER)
    current_user = await service.get(current_user.id)
    await query.answer()
    if isinstance(query.message, Message):
        await query.message.answer(f"Вы авторизованы как <b>{user_role(current_user.role)}</b>")
        await show_menu(current_user=current_user,
                        message=query.message)


@router.message(Command(commands="menu"))
async def command_menu_handler(message: Message, current_user: User, state: FSMContext) -> None:
    await state.clear()
    await show_menu(current_user=current_user,
                    message=message)


@router.callback_query(F.data == "to_menu")
async def to_menu_handler(query: CallbackQuery, current_user: User,  state: FSMContext) -> None:
    await state.clear()
    await query.answer()
    if isinstance(query.message, Message):
        await show_menu(current_user=current_user,
                        message=query.message,
                        replace_text=True)


@router.message(Command(commands="help"))
async def help_handler(message: types.Message, state: FSMContext) -> Message:
    await state.clear()
    return await message.answer("Здесь будет раздел помощи")


@router.callback_query(F.data == "_")
async def do_nothing_callback(query: CallbackQuery) -> None:
    await query.answer()


@router.error(ExceptionTypeFilter(AccessDeniedError), F.update.message.as_("message"))
async def handle_access_error(event: ErrorEvent, message: Message) -> None:
    await message.answer(str(event.exception))


@router.error(ExceptionTypeFilter(ValidationError), F.update.message.as_("message"))
async def handle_validation_error(event: ErrorEvent, message: Message) -> None:
    await message.answer(str(event.exception))


@router.error(ExceptionTypeFilter(InvalidStateError), F.update.message.as_("message"))
async def handle_invalid_state_error(message: Message) -> None:
    await message.answer("Невозможно выполнить действие")

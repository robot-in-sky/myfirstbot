from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.user import User, UserRole
from src.tgbot.views.menu import show_menu, signin_menu_kb
from src.tgbot.views.user.user import user_role

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
async def signin_as_callback(query: CallbackQuery, deps: Dependencies, current_user: User) -> None:
    users = deps.users(current_user)
    match query.data:
        case "signin_as:agent":
            await users.set_role(current_user.id, UserRole.AGENT)
        case "signin_as:user" | _:
            await users.set_role(current_user.id, UserRole.USER)
    current_user = await users.get(current_user.id)
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

"""
@router.message(F.photo)
async def echo_photo_message(message: Message, bot: Bot, deps: Dependencies) -> None:
    if message.photo:
        wait_message = await message.answer("Пожалуйста, подождите...")
        photo = await bot.download(message.photo[-1])
        data = bytes(photo.read())
        recognition_id = uuid7()
        await deps.attachments.add_bytes(recognition_id, PassportFiles.SOURCE, data)
        result_dict = await deps.rpc.proxy.recognize_passport(id_=str(recognition_id))
        result = RecognitionResult(**result_dict)
        await wait_message.delete()
        details = result.details
        lines = [
            f"<b>Фамилия:</b> {details.surname}",
            f"<b>Имя:</b> {details.given_name}",
            f"<b>Пол:</b> {details.gender}",
            f"<b>Дата рождения:</b> {details.birth_date}",
            f"<b>Место рождения:</b> {details.birth_place}",
            f"<b>Номер паспорта:</b> {details.passport_no}",
            f"<b>Страна выдачи:</b> {details.country}",
            f"<b>Дата выдачи:</b> {details.issue_date}",
            f"<b>Действителен до:</b> {details.expire_date}",
        ]
        output = "\n".join(lines)
        await message.answer(output)
        attachments = await asyncio.gather(
            deps.attachments.get_bytes(recognition_id, PassportFiles.SCANNED),
            deps.attachments.get_bytes(recognition_id, PassportFiles.PHOTO),
            deps.attachments.get_bytes(recognition_id, PassportFiles.DEBUG),
        )
        media = [
            InputMediaPhoto(media=BufferedInputFile(attachments[0], PassportFiles.SCANNED)),
            InputMediaPhoto(media=BufferedInputFile(attachments[1], PassportFiles.PHOTO)),
            InputMediaPhoto(media=BufferedInputFile(attachments[2], PassportFiles.DEBUG)),
        ]
        await message.answer_media_group(media)
"""

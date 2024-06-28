from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import UserService
from myfirstbot.tgbot.buttons import USERS
from myfirstbot.tgbot.callbacks import UsersCallbackData
from myfirstbot.tgbot.views.user.users import show_users

router = Router()


@router.message(F.text == USERS)
async def users_button_handler(
        message: Message, db: Database, current_user: User) -> None:
    callback_data = UsersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    result = await UserService(db, current_user).get_all(**params)
    await show_users(result, callback_data,
                     current_user=current_user,
                     message=message)


@router.callback_query(UsersCallbackData.filter())
async def users_query_callback(
        query: CallbackQuery,
        callback_data: UsersCallbackData,
        db: Database,
        current_user: User,
) -> None:
    await query.answer()
    params = callback_data.model_dump(exclude_none=True)
    result = await UserService(db, current_user).get_all(**params)
    await show_users(result, callback_data,
                     current_user=current_user,
                     message=query.message)

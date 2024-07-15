from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService, UserService
from myfirstbot.tgbot.callbacks import UserCallbackData
from myfirstbot.tgbot.views.user.user import show_user

router = Router()


@router.callback_query(UserCallbackData.filter(~F.action))
async def user_callback_handler(
        query: CallbackQuery,
        callback_data: UserCallbackData,
        db: Database,
        current_user: User,
) -> None:
    user = await UserService(db, current_user).get(callback_data.id)
    order_count = await OrderService(db, current_user).get_count(user.id)
    await query.answer()
    if isinstance(query.message, Message):
        await show_user(user,
                        order_count,
                        current_user=current_user,
                        message=query.message)

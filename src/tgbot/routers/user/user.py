from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.entities import User
from src.entities.order import OrderQuery
from src.repositories.utils import Database
from src.services import OrderService, UserService
from src.tgbot.callbacks import UserCallbackData
from src.tgbot.filters import IsAdmin
from src.tgbot.views.user.user import show_user

router = Router()


@router.callback_query(UserCallbackData.filter(~F.action), IsAdmin())
async def user_callback_handler(
        query: CallbackQuery,
        callback_data: UserCallbackData,
        db: Database,
        current_user: User,
) -> None:
    user = await UserService(db, current_user).get(callback_data.id)
    order_count = await OrderService(db, current_user).get_count(OrderQuery(user_id=user.id))
    await query.answer()
    if isinstance(query.message, Message):
        await show_user(user,
                        order_count,
                        current_user=current_user,
                        message=query.message)

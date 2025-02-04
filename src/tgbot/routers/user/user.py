from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities import User
from src.entities.order import OrderQuery
from src.tgbot.callbacks import UserCallbackData
from src.tgbot.filters import IsAdmin
from src.tgbot.views.user.user import show_user

router = Router()


@router.callback_query(UserCallbackData.filter(~F.action), IsAdmin())
async def user_callback_handler(
        query: CallbackQuery,
        callback_data: UserCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    user = await deps.users(current_user).get(callback_data.id)
    order_count = await deps.orders(current_user).get_count(OrderQuery(user_id=user.id))
    await query.answer()
    if isinstance(query.message, Message):
        await show_user(user,
                        order_count,
                        current_user=current_user,
                        message=query.message)

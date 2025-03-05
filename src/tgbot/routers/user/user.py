from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.users import User
from src.tgbot.callbacks import UserCallbackData
from src.tgbot.filters import IsAdmin
from src.tgbot.views.users.user import show_user

router = Router()


@router.callback_query(UserCallbackData.filter(~F.action), IsAdmin())
async def user_callback_handler(
        query: CallbackQuery,
        callback_data: UserCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    users = deps.get_admin_user_service(current_user)
    user = await users.get_user(callback_data.id)
    visa_forms =
    order_count = await deps.orders(current_user).get_count(OrderQuery(user_id=user.id))
    await query.answer()
    if isinstance(query.message, Message):
        await show_user(user,
                        order_count,
                        current_user=current_user,
                        message=query.message)

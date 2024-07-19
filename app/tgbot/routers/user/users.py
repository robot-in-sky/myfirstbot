from aiogram import F, Router
from aiogram.filters import and_f
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery, Message

from app.entities.user import User
from app.repo.utils import Database
from app.services import UserService
from app.tgbot.buttons import USERS
from app.tgbot.callbacks import UserFilterCallbackData, UserSearchCallbackData, UsersCallbackData
from app.tgbot.filters import IsAdmin
from app.tgbot.scenes import SearchUserScene
from app.tgbot.views.user.users import show_user_filter, show_users, users_result_kb

router = Router()
scene_registry = SceneRegistry(router)


@router.message(F.text == USERS, IsAdmin())
async def users_button_handler(
        message: Message, db: Database, current_user: User) -> None:
    callback_data = UsersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    result = await UserService(db, current_user).get_all(**params)
    await show_users(result,
                     callback_data,
                     message=message)


@router.callback_query(UsersCallbackData.filter(), IsAdmin())
async def users_callback_handler(
        query: CallbackQuery,
        callback_data: UsersCallbackData,
        db: Database,
        current_user: User,
) -> None:
    params = callback_data.model_dump(exclude_none=True)
    result = await UserService(db, current_user).get_all(**params)
    await query.answer()
    if isinstance(query.message, Message):
        if callback_data.page:
                await query.message.edit_reply_markup(
                    reply_markup=users_result_kb(result, callback_data))
        else:
            await show_users(result,
                             callback_data,
                             message=query.message,
                             replace_text=True)


scene_registry.add(SearchUserScene)
router.callback_query.register(
    SearchUserScene.as_handler(),
    and_f(UserSearchCallbackData.filter(), IsAdmin()))


@router.callback_query(UserFilterCallbackData.filter(), IsAdmin())
async def user_filter_callback_handler(
        query: CallbackQuery,
        callback_data: UserFilterCallbackData,
        db: Database,
        current_user: User,
) -> None:
    await query.answer()
    if isinstance(query.message, Message):
        service = UserService(db, current_user)
        params = callback_data.model_dump(
            exclude_none=True,
            exclude={"role", "page", "per_page"},
        )
        count_by_status = await service.get_count_by_role(**params)
        total_count = await service.get_count(**params)
        await show_user_filter(count_by_status,
                               total_count,
                               callback_data,
                               message=query.message,
                               replace_text=True)

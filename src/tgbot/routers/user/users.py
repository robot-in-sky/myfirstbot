from aiogram import F, Router
from aiogram.filters import and_f
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.users import User, UserQuery, UserQueryPaged
from src.tgbot.callbacks import UserFilterCallbackData, UserSearchCallbackData, UsersCallbackData
from src.tgbot.filters import IsAdmin
from src.tgbot.scenes import SearchUserScene
from src.tgbot.views.buttons import USERS
from src.tgbot.views.users.users import show_user_filter, show_users, users_result_kb

router = Router()
scene_registry = SceneRegistry(router)


@router.message(F.text == USERS, IsAdmin())
async def users_button_handler(
        message: Message, deps: Dependencies, current_user: User) -> None:
    callback_data = UsersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    users = deps.get_admin_user_service(current_user)
    result = await users.get_users(UserQueryPaged(**params))
    await show_users(result,
                     callback_data,
                     message=message)


@router.callback_query(UsersCallbackData.filter(), IsAdmin())
async def users_callback_handler(
        query: CallbackQuery,
        callback_data: UsersCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    params = callback_data.model_dump(exclude_none=True)
    users = deps.get_admin_user_service(current_user)
    result = await users.get_users(UserQueryPaged(**params))
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
        deps: Dependencies,
        current_user: User,
) -> None:
    await query.answer()
    if isinstance(query.message, Message):
        users = deps.get_admin_user_service(current_user)
        params = callback_data.model_dump(
            exclude_none=True,
            exclude={"role", "page", "per_page"},
        )
        count_by_status = await users.get_user_count_by_role(UserQuery(**params))
        total_count = await users.get_user_count(UserQuery(**params))
        await show_user_filter(count_by_status,
                               total_count,
                               callback_data,
                               message=query.message,
                               replace_text=True)

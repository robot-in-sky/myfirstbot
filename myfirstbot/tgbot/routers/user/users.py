from aiogram import F, Router
from aiogram.fsm.scene import SceneRegistry
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import UserService
from myfirstbot.tgbot.buttons import USERS
from myfirstbot.tgbot.callbacks import UserFilterCallbackData, UserSearchCallbackData, UsersCallbackData
from myfirstbot.tgbot.scenes import SearchUserScene
from myfirstbot.tgbot.views.user.users import show_user_filter, show_users, users_result_kb

router = Router()
scene_registry = SceneRegistry(router)


@router.message(F.text == USERS)
async def users_button_handler(
        message: Message, db: Database, current_user: User) -> None:
    callback_data = UsersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    result = await UserService(db, current_user).get_all(**params)
    await show_users(result,
                     callback_data,
                     message=message)


@router.callback_query(UsersCallbackData.filter())
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
    SearchUserScene.as_handler(), UserSearchCallbackData.filter())


@router.callback_query(UserFilterCallbackData.filter())
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

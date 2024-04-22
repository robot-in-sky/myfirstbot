from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message

# import get_user_repo, get_order_repo

start_router = Router(name="start")


@start_router.message(CommandStart())
async def start_handler(message: types.Message) -> Message:
    # user_repo = UserRepo()
    # await user_repo.get_by_username(data["username"])
    return await message.answer("Привет! Здесь будут команды бота")


from aiogram import Bot
from aiogram.types import BotCommand

START = "start"
MENU = "menu"
HELP = "help"

COMMANDS = [
    BotCommand(command=START, description="Запустить бота"),
    BotCommand(command=MENU, description="Главное меню"),
    BotCommand(command=HELP, description="Помощь"),
]

async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(commands=COMMANDS)

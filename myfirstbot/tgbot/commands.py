from aiogram.types import BotCommand

START = "start"
MENU = "menu"
HELP = "help"

COMMANDS = [
    BotCommand(command=MENU, description="Главное меню"),
    BotCommand(command=HELP, description="Помощь"),
]

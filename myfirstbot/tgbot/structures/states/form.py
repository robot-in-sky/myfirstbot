from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()

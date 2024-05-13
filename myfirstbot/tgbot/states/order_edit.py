from aiogram.fsm.state import State, StatesGroup


class OrderEditState(StatesGroup):
    intro = State()
    label = State()
    size = State()
    qty = State()
    confirm = State()

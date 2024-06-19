from aiogram.fsm.state import State, StatesGroup


class NewOrderState(StatesGroup):
    label = State()
    size = State()
    qty = State()

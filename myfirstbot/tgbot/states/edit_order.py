from aiogram.fsm.state import State, StatesGroup


class EditOrderState(StatesGroup):
    label = State()
    size = State()
    qty = State()


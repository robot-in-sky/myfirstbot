from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from myfirstbot.entities.order import OrderAdd
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AppError
from myfirstbot.repo.utils.database import Database
from myfirstbot.services.common.my_orders import MyOrdersService
from myfirstbot.tgbot.states import EditOrderState
from myfirstbot.tgbot.views.common.my_orders import order_summary, order_actions_kb

router = Router()


@router.message(EditOrderState.label)
async def order_edit_state_label_handler(message: Message, state: FSMContext) -> None:
    if len(message.text) > 20:
        await message.answer("Длина надписи не более 20 символов. Попробуйте ещё раз.")
        return
    await state.update_data(label=message.text)
    await state.set_state(EditOrderState.size)
    await message.answer(
        "Выберите размер:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="42"),
                    KeyboardButton(text="46"),
                    KeyboardButton(text="50"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


@router.message(EditOrderState.size)
async def order_edit_state_size_handler(message: Message, state: FSMContext) -> None:
    if message.text not in ["42", "46", "50"]:
        await message.answer("Доступные размеры: 42, 46, 50. Попробуйте ещё раз.")
        return
    await state.update_data(size=int(message.text))
    await state.set_state(EditOrderState.qty)
    await message.answer(
        "Укажите количество:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(EditOrderState.qty)
async def order_edit_state_qty_handler(
        message: Message,
        state: FSMContext,
        db: Database,
        user: User,
) -> None:
    data = {"user_id": user.id}
    try:
        value = int(message.text)
        if value > 0:
            data = data | await state.update_data(qty=value)
        else:
            await message.answer("Введите положительное число")
            return
    except (TypeError, ValueError):
        await message.answer("Введите целое число")
        return

    try:
        order = await MyOrdersService(db, user).new(OrderAdd(**data))
        await message.answer(
            (f"Заказ #{order.id} успешно создан.\n"
             f"Проверьте данные:\n\n" +
            order_summary(order, user)),
            reply_markup=order_actions_kb(order, user),
        )
        await state.clear()
    except AppError:
        await message.answer("При добавлении заказа произошла ошибка")

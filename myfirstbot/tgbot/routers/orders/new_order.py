from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from myfirstbot.entities.order import OrderAdd
from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot import buttons
from myfirstbot.tgbot.editors.order_editor import order_editor
from myfirstbot.tgbot.states import NewOrderState
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.orders.order import order_actions_kb, order_summary

router = Router()


@router.message(F.text == buttons.NEW_ORDER)
async def new_order_button_handler(message: Message) -> None:
    await message.answer(
        "Пусть в качестве заказа будут, например, футболки.\n"
        "Кастомными параметрами заказа будут надпись, размер и количество.\n",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons.BACK, callback_data="new_order:back"),
                InlineKeyboardButton(text=buttons.NEXT, callback_data="new_order:next")],
            ],
        ),
    )


@router.callback_query(F.data == "new_order:back")
async def new_order_back_callback(query: CallbackQuery, user: User) -> None:
    await query.answer()
    await query.message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb(user),
    )


@router.callback_query(F.data == "new_order:next")
async def new_order_next_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await state.set_state(NewOrderState.label)
    await order_editor.show_input("label", query.message)


@router.message(NewOrderState.label)
async def new_order_state_label_handler(message: Message, state: FSMContext) -> None:
    await order_editor.validate_input("label", state, message)
    await state.set_state(NewOrderState.size)
    await order_editor.show_input("size", message)


@router.message(NewOrderState.size)
async def new_order_state_size_handler(message: Message, state: FSMContext) -> None:
    await order_editor.validate_input("size", state, message)
    await state.set_state(NewOrderState.qty)
    await order_editor.show_input("qty", message)


@router.message(NewOrderState.qty)
async def new_order_state_qty_handler(
        message: Message,
        state: FSMContext,
        db: Database,
        user: User,
) -> None:
    await order_editor.validate_input("qty", state, message)

    data = (await state.get_data()) | {"user_id": user.id}
    order = await OrderService(db, user).new(OrderAdd(**data))
    await state.clear()
    await message.answer(
        ("<i>Заказ успешно создан.</i>\n"
         "<i>Проверьте данные:</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )

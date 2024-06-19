from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot import buttons
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.orders.orders import order_items_kb

router = Router()


@router.message(F.text == buttons.MY_ORDERS)
async def my_orders_button_handler(message: Message, db: Database, user: User) -> None:
    _message = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
    my_orders = await OrderService(db, user).get_my(per_page=6)
    await _message.delete()

    if len(my_orders.items) > 0:
        await message.answer(
            "Мои заказы:",
            reply_markup=order_items_kb(my_orders, user, "my_orders"),
        )
    else:
        await message.answer(
            "Заказов не найдено",
            reply_markup=main_menu_kb(user),
        )


@router.callback_query(F.data.startswith("my_orders:page_"))
async def my_orders_pagination_callback(query: CallbackQuery, db: Database, user: User) -> None:
    page = int(query.data.split(":")[-1])
    my_orders = await OrderService(db, user).get_all(per_page=6, page=page)
    await query.message.edit_reply_markup(
        reply_markup=order_items_kb(my_orders, user, "my_orders")
    )


@router.message(F.text == buttons.ORDERS)
async def all_orders_button_handler(message: Message, db: Database, user: User) -> None:
    _message = await message.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
    my_orders = await OrderService(db, user).get_all(per_page=6)
    await _message.delete()

    if len(my_orders.items) > 0:
        await message.answer(
            "Все заказы:",
            reply_markup=order_items_kb(my_orders, user, "manage_orders"),

        )
    else:
        await message.answer(
            "Заказов не найдено",
            reply_markup=main_menu_kb(user)
        )


@router.callback_query(F.data.startswith("manage_orders:page_"))
async def all_orders_pagination_callback(query: CallbackQuery, db: Database, user: User) -> None:
    page = int(query.data.split(":")[-1])
    my_orders = await OrderService(db, user).get_all(per_page=6, page=page)
    await query.message.edit_reply_markup(
        reply_markup=order_items_kb(my_orders, user, "manage_orders")
    )

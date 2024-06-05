from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import MyOrdersService
from myfirstbot.tgbot.states import EditOrderState
from myfirstbot.tgbot.views.common import buttons
from myfirstbot.tgbot.views.common.main_menu import main_menu_kb
from myfirstbot.tgbot.views.common.my_orders import order_actions_kb, order_items_kb, order_summary

router = Router()

@router.message(F.text == buttons.NEW_ORDER)
async def new_order_button_handler(message: Message) -> None:
    await message.answer(
        "Пусть в качестве заказа будут, например, футболки.\n"
        "Кастомными параметрами заказа будут надпись, размер и количество.\n",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons.NEXT, callback_data="new_order:next"),
                 InlineKeyboardButton(text=buttons.BACK, callback_data="new_order:back")],
            ],
        ),
    )

@router.callback_query(F.data == "new_order:next")
async def new_order_next_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditOrderState.label)
    await query.answer()
    await query.message.answer(
        "Какую бы Вы хотели надпись? Введите текст:",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.callback_query(F.data == "new_order:back")
async def my_orders_back_callback(query: CallbackQuery, user: User) -> None:
    await query.answer()
    await query.message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb(user),
    )

@router.message(F.text == buttons.MY_ORDERS)
async def my_orders_button_handler(message: Message, db: Database, user: User) -> None:
    my_orders = await MyOrdersService(db, user).get_all(per_page=6)
    if len(my_orders.items) > 0:
        await message.answer(
            "Мои заказы:",
            reply_markup=order_items_kb(my_orders),
        )
    else:
        await message.answer(
            "Результатов не найдено",
            reply_markup=main_menu_kb(user)
        )

@router.callback_query(F.data.startswith("my_orders:page_"))
async def my_orders_page_callback(
        query: CallbackQuery, db: Database,
        user: User, bot: Bot
) -> None:
    page = int(query.data.split(":")[-1])
    my_orders = await MyOrdersService(db, user).get_all(per_page=6, page=page)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=order_items_kb(my_orders)
    )

@router.callback_query(F.data.startswith("my_orders:order:get:"))
async def my_orders_get_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order = await MyOrdersService(db, user).get(order_id)
    await query.answer()
    await query.message.answer(
        (f"Заказ #{order.id}:\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )

@router.callback_query(F.data.startswith("my_orders:order:submit:"))
async def my_orders_submit_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await MyOrdersService(db, user).submit(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} отправлен на проверку\n"
        "Ждите подтверждения",
        reply_markup=main_menu_kb(user),
    )

@router.callback_query(F.data.startswith("my_orders:order:return:"))
async def my_orders_return_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = MyOrdersService(db, user)
    order_id = await service.return_(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} возвращен на доработку",
        reply_markup=order_actions_kb(order, user),
    )

@router.callback_query(F.data.startswith("my_orders:order:trash:"))
async def my_orders_trash_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await MyOrdersService(db, user).trash(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} удалён",
        reply_markup=main_menu_kb(user),
    )

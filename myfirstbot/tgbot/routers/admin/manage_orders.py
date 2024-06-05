from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.user import User
from myfirstbot.repo.utils.database import Database
from myfirstbot.services import ManageOrdersService
from myfirstbot.tgbot.views.common import buttons
from myfirstbot.tgbot.views.common.main_menu import main_menu_kb
from myfirstbot.tgbot.views.common.my_orders import order_actions_kb, order_items_kb, order_summary

router = Router()

@router.message(F.text == buttons.ORDERS)
async def manage_orders_button_handler(message: Message, db: Database, user: User) -> None:
    my_orders = await ManageOrdersService(db, user).get_all(per_page=6)
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

@router.callback_query(F.data.startswith("manage_orders:page_"))
async def manage_orders_pagination_callback(
        query: CallbackQuery, db: Database,
        user: User, bot: Bot
) -> None:
    page = int(query.data.split(":")[-1])
    my_orders = await ManageOrdersService(db, user).get_all(per_page=6, page=page)
    await bot.edit_message_reply_markup(
        query.message.chat.id,
        query.message.message_id,
        reply_markup=order_items_kb(my_orders)
    )

@router.callback_query(F.data.startswith("manage_orders:order:get:"))
async def manage_orders_get_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order = await ManageOrdersService(db, user).get(order_id)
    await query.answer()
    await query.message.answer(
        (f"Заказ #{order.id}:\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )

@router.callback_query(F.data.startswith("manage_orders:order:accept:"))
async def manage_orders_accept_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = ManageOrdersService(db, user)
    order_id = await service.accept(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.answer(
        (f"Заказ #{order.id} взят в работу:\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )

@router.callback_query(F.data.startswith("manage_orders:order:reject:"))
async def manage_orders_reject_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = ManageOrdersService(db, user).reject(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} возвращен на доработку",
        reply_markup=main_menu_kb(user),
    )

@router.callback_query(F.data.startswith("manage_orders:order:trash:"))
async def manage_orders_trash_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await ManageOrdersService(db, user).trash(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} перемещён в корзину",
        reply_markup=main_menu_kb(user),
    )

@router.callback_query(F.data.startswith("manage_orders:order:restore:"))
async def manage_orders_restore_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = ManageOrdersService(db, user)
    order_id = await service.restore(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.answer(
        (f"Заказ #{order.id} восстановлен:\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )

@router.callback_query(F.data.startswith("manage_orders:order:delete:"))
async def manage_orders_delete_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await ManageOrdersService(db, user).delete(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} удалён",
        reply_markup=main_menu_kb(user),
    )

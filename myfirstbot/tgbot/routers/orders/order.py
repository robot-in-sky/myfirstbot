from aiogram import F, Router
from aiogram.types import CallbackQuery

from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.views.menu import main_menu_kb
from myfirstbot.tgbot.views.ok_cancel import ok_cancel_kb
from myfirstbot.tgbot.views.orders.order import order_actions_kb, order_summary

router = Router()


@router.callback_query(F.data.startswith("order:get:"))
async def order_get_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order = await OrderService(db, user).get(order_id)
    await query.answer()
    await query.message.answer(
        order_summary(order, user),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:submit:"))
async def order_submit_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = OrderService(db, user)
    order_id = await service.submit(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ отправлен на проверку</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:return:"))
async def order_return_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = OrderService(db, user)
    order_id = await service.return_(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ возвращен на доработку</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:trash:"))
async def order_trash_callback(query: CallbackQuery, db: Database, user: User) -> None:
    query_data = query.data.split(":")
    order_id = int(query_data[2])
    await query.answer()
    if len(query_data) <= 3:
        await query.message.edit_text(
            "Вы уверены что хотите удалить заказ?",
            reply_markup=ok_cancel_kb(f"order:trash:{order_id}"),
        )
    else:
        action = query.data.split(":")[3]
        if action == "ok":
            order_id = await OrderService(db, user).trash(order_id)
            await query.message.answer(
                f"Заказ #{order_id} удалён",
                reply_markup=main_menu_kb(user),
            )
        elif action == "cancel":
            await query.message.delete()


@router.callback_query(F.data.startswith("order:accept:"))
async def order_accept_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = OrderService(db, user)
    order_id = await service.accept(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ взят в работу</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:reject:"))
async def order_reject_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = OrderService(db, user)
    order_id = await service.reject(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ возвращён на доработку</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:done:"))
async def order_done_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = OrderService(db, user)
    order_id = await service.done(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ завершён</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:restore:"))
async def order_restore_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = OrderService(db, user)
    order_id = await service.restore(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ восстановлен</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data.startswith("order:delete:"))
async def order_delete_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await OrderService(db, user).delete(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} удалён окончательно",
        reply_markup=main_menu_kb(user),
    )


@router.callback_query(F.data.startswith("order:menu"))
async def order_back_callback(query: CallbackQuery, user: User) -> None:
    await query.answer()
    await query.message.answer(
        "Главное меню",
        reply_markup=main_menu_kb(user),
    )

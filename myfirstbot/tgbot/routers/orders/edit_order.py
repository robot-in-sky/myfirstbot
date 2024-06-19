from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from myfirstbot.entities.order import OrderUpdate
from myfirstbot.entities.user import User
from myfirstbot.repo.utils import Database
from myfirstbot.services import OrderService
from myfirstbot.tgbot.editors.order_editor import order_editor
from myfirstbot.tgbot.states import EditOrderState
from myfirstbot.tgbot.views.orders.order import order_actions_kb, order_summary

router = Router()


@router.callback_query(F.data.startswith("edit_order:start:"))
async def edit_order_start_callback(
        query: CallbackQuery, state: FSMContext, db: Database, user: User,
) -> None:
    order_id = int(query.data.split(":")[-1])
    order = await OrderService(db, user).get(order_id)
    order_dict = order.model_dump()
    field_ids = ["id", *order_editor.field_ids, "status"]
    data = {id_: order_dict[id_] for id_ in field_ids}
    await query.answer()
    await state.set_data(data)
    await state.set_state(EditOrderState.label)
    await order_editor.refresh_editor("label", state, query.message)


@router.callback_query(EditOrderState.label, F.data.startswith("field:"))
async def edit_order_label_field_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    if query.data == "field:prev":
        await state.set_state(EditOrderState.qty)
        await order_editor.refresh_editor("qty", state, query.message)
    if query.data == "field:edit":
        await order_editor.show_input("label", query.message)
    if query.data == "field:next":
        await state.set_state(EditOrderState.size)
        await order_editor.refresh_editor("size", state, query.message)


@router.message(EditOrderState.label)
async def edit_order_state_label_handler(message: Message, state: FSMContext) -> None:
    await order_editor.validate_input("label", state, message)
    await order_editor.show_editor("label", state, message)


@router.callback_query(EditOrderState.size, F.data.startswith("field:"))
async def edit_order_size_field_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    if query.data == "field:prev":
        await state.set_state(EditOrderState.label)
        await order_editor.refresh_editor("label", state, query.message)
    if query.data == "field:edit":
        await order_editor.show_input("size", query.message)
    if query.data == "field:next":
        await state.set_state(EditOrderState.qty)
        await order_editor.refresh_editor("qty", state, query.message)


@router.message(EditOrderState.size)
async def edit_order_state_size_handler(message: Message, state: FSMContext) -> None:
    await order_editor.validate_input("size", state, message)
    await order_editor.show_editor("size", state, message)


@router.callback_query(EditOrderState.qty, F.data.startswith("field:"))
async def edit_order_qty_field_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    if query.data == "field:prev":
        await state.set_state(EditOrderState.size)
        await order_editor.refresh_editor("size", state, query.message)
    if query.data == "field:edit":
        await order_editor.show_input("qty", query.message)
    if query.data == "field:next":
        await state.set_state(EditOrderState.label)
        await order_editor.refresh_editor("label", state, query.message)


@router.message(EditOrderState.qty)
async def edit_order_state_qty_handler(message: Message, state: FSMContext) -> None:
    await order_editor.validate_input("qty", state, message)
    await order_editor.show_editor("qty", state, message)


@router.callback_query(F.data == "edit_order:cancel")
async def edit_order_cancel_callback(
        query: CallbackQuery,
        state: FSMContext,
        db: Database,
        user: User,
) -> None:
    data = await state.get_data()
    order_id = data["id"]
    order = await OrderService(db, user).get(order_id)
    await state.clear()
    await query.answer()
    await query.message.edit_text(
        order_summary(order, user),
        reply_markup=order_actions_kb(order, user),
    )


@router.callback_query(F.data == "edit_order:save")
async def order_edit_save_callback(
        query: CallbackQuery,
        state: FSMContext,
        db: Database,
        user: User,
) -> None:
    data = await state.get_data()
    order_id = data["id"]
    field_ids = order_editor.field_ids
    update = {id_: data[id_] for id_ in field_ids}
    order = await OrderService(db, user).update(order_id, OrderUpdate(**update))
    await state.clear()
    await query.answer()
    await query.message.edit_text(
        ("<i>Заказ успешно обновлён</i>\n\n" +
        order_summary(order, user)),
        reply_markup=order_actions_kb(order, user),
    )


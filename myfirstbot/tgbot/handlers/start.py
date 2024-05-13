from collections.abc import Sequence

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from myfirstbot.base.repo.sql.database import Database
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderAdd
from myfirstbot.entities.user import User
from myfirstbot.exceptions import AppError
from myfirstbot.services.my_orders import MyOrdersService
from myfirstbot.tgbot.states.order_edit import OrderEditState

start_router = Router(name="start")

NEW_ORDER = "➕ Создать заказ"
MY_ORDERS = "📦 Мои заказы"

NEXT = "➡ Далее"
BACK = "↩ Назад"

SUBMIT = "✅ Подтвердить"
EDIT = "✏️ Изменить"
RETURN = "↩ Вернуть на доработку"
TRASH = "🗑️ Удалить"
DELETE = "✖️ Удалить"
AGENT = "👤 Задать вопрос агенту"


MAIN_MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=NEW_ORDER), KeyboardButton(text=MY_ORDERS)]],
    resize_keyboard=True,
)


def shorten_string(string: str, limit: int = 10) -> str:
    return f"{string[:limit]}…" if len(string) > limit else string


def order_status_output(status: OrderStatus) -> str:
    return {
        status.TRASH: "Удалён",
        status.DRAFT: "Черновик",
        status.PENDING: "На проверке",
        status.ACCEPTED: "Принят",
        status.COMPLETED: "Завершён",
    }.get(status, f"<{status}>")


def order_summary(order: Order) -> str:
    return (
        f"Надпись: {order.label}\n"
        f"Размер: {order.size}\n"
        f"Количество: {order.qty}\n\n"
        f"Статус: {order_status_output(order.status)}"
    )


def order_kb_markup(order: Order) -> InlineKeyboardMarkup:
    keyboard = []
    if order.status == OrderStatus.DRAFT:
        keyboard.append([InlineKeyboardButton(
            text=SUBMIT, callback_data=f"my_orders:order:submit:{order.id}")])
        keyboard.append([InlineKeyboardButton(
            text=EDIT, callback_data=f"my_orders:order:edit:{order.id}")])
        keyboard.append([InlineKeyboardButton(
            text=DELETE, callback_data=f"my_orders:order:trash:{order.id}")])
    if order.status == OrderStatus.PENDING:
        keyboard.append([InlineKeyboardButton(
            text=RETURN, callback_data=f"my_orders:order:return:{order.id}")])
    if order.status == OrderStatus.ACCEPTED:
        keyboard.append([InlineKeyboardButton(
            text=AGENT, callback_data=f"my_orders:order:agent:{order.id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def order_item_output(order: Order) -> str:
    max_width = 45
    delim_chars = 10
    id_ = f"#{order.id}"
    size = f"({order.size})"
    qty = f"{order.qty} шт."
    status = order_status_output(order.status)
    label_limit = max_width - len(id_) - len(size) - len(qty) - len(status) - delim_chars
    label = f"{shorten_string(order.label, label_limit)}"
    return f"{id_} | {label} {size} | {qty} | {status}"


def orders_kb_markup(orders: Sequence[Order]) -> InlineKeyboardMarkup:
    keyboard = []
    for order in orders:
        item = order_item_output(order)
        data = f"my_orders:order:get:{order.id}"
        keyboard.append([InlineKeyboardButton(text=item, callback_data=data)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@start_router.message(CommandStart())
async def command_start_handler(message: Message, user: User) -> None:
    await message.answer(
        f"Приветствую, {user.user_name}!\n"
        "Я — тестовый бот-пример для управления заказами",
        reply_markup=MAIN_MENU_BOARD,
    )


@start_router.message(Command("menu"))
async def command_menu_handler(message: Message) -> None:
    await message.answer(
        "Главное меню:",
        reply_markup=MAIN_MENU_BOARD,
    )


@start_router.message(F.text == NEW_ORDER)
async def new_order_button_handler(message: Message) -> None:
    await message.answer(
        "Пусть в качестве заказа будут, например, футболки.\n"
        "Кастомными параметрами заказа будут надпись, размер и количество.\n",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=NEXT, callback_data="new_order:next"),
                 InlineKeyboardButton(text=BACK, callback_data="new_order:back")]
            ],
        ),
    )


@start_router.callback_query(F.data == "new_order:back")
async def new_order_back_callback(query: CallbackQuery) -> None:
    await query.answer()
    await query.message.answer(
        "Главное меню:",
        reply_markup=MAIN_MENU_BOARD,
    )


@start_router.callback_query(F.data == "new_order:next")
async def new_order_next_callback(query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(OrderEditState.label)
    await query.answer()
    await query.message.answer(
        "Какую бы Вы хотели надпись? Введите текст:",
        reply_markup=ReplyKeyboardRemove(),
    )


@start_router.message(OrderEditState.label)
async def order_edit_state_label_handler(message: Message, state: FSMContext) -> None:
    if len(message.text) > 20:
        await message.answer("Длина надписи не более 20 символов. Попробуйте ещё раз.")
        return
    await state.update_data(label=message.text)
    await state.set_state(OrderEditState.size)
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


@start_router.message(OrderEditState.size)
async def order_edit_state_size_handler(message: Message, state: FSMContext) -> None:
    if message.text not in ["42", "46", "50"]:
        await message.answer("Доступные размеры: 42, 46, 50. Попробуйте ещё раз.")
        return
    await state.update_data(size=int(message.text))
    await state.set_state(OrderEditState.qty)
    await message.answer(
        "Укажите количество:",
        reply_markup=ReplyKeyboardRemove(),
    )


@start_router.message(OrderEditState.qty)
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
            order_summary(order)),
            reply_markup=order_kb_markup(order)
        )
        await state.clear()
    except AppError:
        await message.answer("При добавлении заказа произошла ошибка")


@start_router.message(F.text == MY_ORDERS)
async def my_orders_button_handler(message: Message, db: Database, user: User) -> None:
    my_orders = await MyOrdersService(db, user).get_all(limit=10)
    await message.answer(
        "Мои заказы:",
        reply_markup=orders_kb_markup(my_orders),
    )


@start_router.message(F.text == F.data.startswith("my_orders:page:"))
async def my_orders_page_callback(query: CallbackQuery, db: Database, user: User) -> None:
    page = int(query.data.split(":")[-1])
    my_orders = await MyOrdersService(db, user).get_all(limit=10, page=page)
    await query.answer()
    await query.message.answer(
        f"Мои заказы [{page}]:",
        reply_markup=orders_kb_markup(my_orders),
    )


@start_router.callback_query(F.data.startswith("my_orders:order:get:"))
async def my_orders_get_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order = await MyOrdersService(db, user).get(order_id)
    await query.answer()
    await query.message.answer(
        (f"Заказ #{order.id}:\n\n" +
        order_summary(order)),
        reply_markup=order_kb_markup(order)
    )

@start_router.callback_query(F.data.startswith("my_orders:order:submit:"))
async def my_orders_submit_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await MyOrdersService(db, user).submit(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} отправлен на проверку\n"
        "Ждите подтверждения",
        reply_markup=MAIN_MENU_BOARD
    )

@start_router.callback_query(F.data.startswith("my_orders:order:return:"))
async def my_orders_return_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    service = MyOrdersService(db, user)
    order_id = await service.return_(order_id)
    order = await service.get(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} возвращен на доработку",
        reply_markup=order_kb_markup(order)
    )

@start_router.callback_query(F.data.startswith("my_orders:order:trash:"))
async def my_orders_trash_callback(query: CallbackQuery, db: Database, user: User) -> None:
    order_id = int(query.data.split(":")[-1])
    order_id = await MyOrdersService(db, user).trash(order_id)
    await query.answer()
    await query.message.answer(
        f"Заказ #{order_id} удалён",
        reply_markup=MAIN_MENU_BOARD
    )

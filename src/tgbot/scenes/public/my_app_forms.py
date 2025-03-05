from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import SceneRegistry, Scene
from aiogram.types import CallbackQuery, Message

from src.deps import Dependencies
from src.entities.order import OrderQuery, OrderQueryPaged
from src.entities.users import User, UserRole
from src.tgbot.callbacks import OrderFilterCallbackData, OrderSearchCallbackData, OrdersCallbackData
from src.tgbot.scenes import SearchOrderScene
from src.tgbot.views.buttons import MY_APP_FORMS, MANAGE_APP_FORMS
from src.tgbot.views.visas.app_forms import orders_result_kb, show_order_filter, show_orders

router = Router()
scene_registry = SceneRegistry(router)


@router.message(F.text.in_({MY_APP_FORMS, MANAGE_APP_FORMS}))
async def orders_button_handler(
        message: Message,
        deps: Dependencies,
        current_user: User,
) -> None:
    callback_data = OrdersCallbackData()
    params = callback_data.model_dump(exclude_none=True)
    if message.text == MY_APP_FORMS or current_user.role < UserRole.AGENT:
        params["user_id"] = current_user.id
    result = await deps.orders(current_user).get_many(OrderQueryPaged(**params))
    await show_orders(result,
                      callback_data,
                      current_user=current_user,
                      message=message)


@router.callback_query(OrdersCallbackData.filter())
async def orders_callback_handler(
        query: CallbackQuery,
        callback_data: OrdersCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    await query.answer()
    params = callback_data.model_dump(exclude_none=True)
    if current_user.role < UserRole.AGENT:
        params["user_id"] = current_user.id
    result = await deps.orders(current_user).get_many(OrderQueryPaged(**params))
    if isinstance(query.message, Message):
        if callback_data.page:
            await query.message.edit_reply_markup(
                reply_markup=orders_result_kb(result,
                                              callback_data,
                                              current_user=current_user))
        else:
            await show_orders(result,
                              callback_data,
                              current_user=current_user,
                              message=query.message,
                              replace_text=True)


scene_registry.add(SearchOrderScene)
router.callback_query.register(
    SearchOrderScene.as_handler(), OrderSearchCallbackData.filter())


@router.callback_query(OrderFilterCallbackData.filter())
async def order_filter_callback_handler(
        query: CallbackQuery,
        callback_data: OrderFilterCallbackData,
        deps: Dependencies,
        current_user: User,
) -> None:
    await query.answer()
    if isinstance(query.message, Message):
        orders = deps.orders(current_user)
        params = callback_data.model_dump(
            exclude_none=True,
            exclude={"status", "page", "per_page"},
        )
        if current_user.role < UserRole.AGENT:
            params["user_id"] = current_user.id
        count_by_status = await orders.get_count_by_status(OrderQuery(**params))
        total_count = await orders.get_count(OrderQuery(**params))
        await show_order_filter(count_by_status,
                                total_count,
                                callback_data,
                                current_user=current_user,
                                message=query.message,
                                replace_text=True)


class RepeaterScene(Scene, state="repeater"):

    @on.message.enter()
    async def message_on_enter(self,
                               message: Message,
                               state: FSMContext,
                               deps: Dependencies, *,
                               repeater_id: str | None = None,
                               replace: bool = False) -> None:

        data = await state.get_data()

        if repeater_id is not None:
            # Set defaults
            data["repeater.id"] = repeater_id
            data["repeater.item.step"] = 0
            await state.set_data(data)

        result = await deps.orders(current_user).get_many(OrderQueryPaged(**params))
        if isinstance(query.message, Message):
            await show_orders(result,
                              callback_data,
                              current_user=current_user,
                              message=query.message,
                              replace_text=True)


    @on.callback_query.enter()
    async def callback_query_on_enter(self,  # noqa: PLR0913
                                      query: CallbackQuery,
                                      state: FSMContext,
                                      deps: Dependencies, *,
                                      repeater_id: str | None = None,
                                      replace: bool = False) -> None:
        await query.answer()
        if isinstance(query.message, Message):
            await self.message_on_enter(query.message,
                                        state, deps,
                                        repeater_id=repeater_id,
                                        replace=replace)


    @on.callback_query(F.data)
    async def repeater_action_callback(self,
                                       query: CallbackQuery,
                                       state: FSMContext) -> None:
        await query.answer()
        if isinstance(query.message, Message) and query.data.startswith("repeater:"):
                _, action = query.data.split(":")
                data = await state.get_data()
                repeater_id = data["repeater.id"]
                match action:

                    case "add":
                        step_key = f"form.data.{repeater_id}.step"
                        data[step_key] = data[step_key] + 1
                        item_step_key = f"form.data.{repeater_id}.item_step"
                        data[item_step_key] = 0
                        await state.set_data(data)
                        await self.wizard.retake(replace=True)

                    case "reset":
                        # Reset data to default
                        data = remove_keys_by_prefix(data, prefix=f"form.data.{repeater_id}.")
                        await state.set_data(data)
                        await self.wizard.retake(repeater_id=repeater_id, replace=True)

                    case "confirm":
                        # Remove keyboard and show confirmation
                        await query.message.edit_reply_markup(reply_markup=None)
                        await show_repeater_completed(query.message)
                        await asyncio.sleep(0.3)
                        # Switch form step
                        data["form.form_step"] = data["form.form_step"] + 1
                        data["form.section_step"] = 0
                        await state.set_data(data)
                        # Go back to the form scene
                        await self.wizard.goto("fill_form")


    @on.message(F.text)
    async def process_input(self,  # noqa: PLR0912
                            message: Message,
                            state: FSMContext,
                            deps: Dependencies) -> None:

        if message.text:
            data = await state.get_data()
            repeater_id = data["repeater.id"]
            repeater = deps.forms.get_section(repeater_id)
            if not isinstance(repeater, Repeater):
                return

            step_key = f"form.data.{repeater_id}.step"
            item_step_key = f"form.data.{repeater_id}.item_step"
            item_step = data.get(item_step_key, 0)

            if step_key not in data:
                field = repeater.condition_field
            else:
                try:
                    field = repeater.repeater_fields[item_step]
                except IndexError:
                    return

            if field.type == FieldType.CHOICE and message.text == ALL:
                await show_all_options(field, message=message)
                return

            try:
                value = deps.forms.validate_input(field, message.text)
            except ValidationError as error:
                await message.answer(str(error))
                return

            if step_key not in data:
                if value == YesNo.YES:
                    data[step_key] = 0
                else:
                    data[step_key] = -1
            else:
                step = data[step_key]
                data[f"form.data.{repeater_id}.{step}.{field.id}"] = value
                data[item_step_key] = item_step + 1

            await state.set_data(data)
            await self.wizard.retake()

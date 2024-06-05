from myfirstbot.tgbot.handlers.common.commands import router as _commands_router
from myfirstbot.tgbot.handlers.common.edit_order import router as _edit_order_router
from myfirstbot.tgbot.handlers.common.my_orders import router as _my_orders_router

routers = (
    _commands_router,
    _edit_order_router,
    _my_orders_router,
)

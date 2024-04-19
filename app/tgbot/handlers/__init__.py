from .forms import form_router
from .help import help_router
from .start import start_router

routers = (
    form_router,
    help_router,
    start_router
)

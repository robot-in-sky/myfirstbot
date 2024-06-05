from myfirstbot.entities.choices import OrderStatus, UserRole
from myfirstbot.entities.user import User


def is_admin(user: User) -> bool:
    return user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]


def order_status(status: OrderStatus) -> str:
    return {
        status.TRASH: "Удалён",
        status.DRAFT: "Черновик",
        status.PENDING: "На проверке",
        status.ACCEPTED: "Принят",
        status.COMPLETED: "Завершён",
    }.get(status, f"<{status}>")


def cut_string(string: str, limit: int = 10) -> str:
    if 1 < limit < len(string):
        return f"{string[:limit-1]}…"
    return string
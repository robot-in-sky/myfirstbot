from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.user import User


def has_admin_access(user: User) -> bool:
    return user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]
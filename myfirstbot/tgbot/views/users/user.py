from myfirstbot.entities.choices import UserRole
from myfirstbot.entities.user import User


def is_admin(user: User) -> bool:
    return user.role in [UserRole.ADMINISTRATOR, UserRole.AGENT]

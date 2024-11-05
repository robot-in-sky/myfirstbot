from typing import Any

from aiogram.filters import BaseFilter

from src.entities.choices import UserRole


class IsAdmin(BaseFilter):

    async def __call__(self, *args: Any, **kwargs: Any) -> bool:  # noqa: ARG002
        return kwargs["current_user"].role >= UserRole.AGENT

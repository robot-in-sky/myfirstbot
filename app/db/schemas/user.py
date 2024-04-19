from pydantic import ConfigDict

from .base import BaseSchema
# from .order import OrderSchema
from app.db.types.access_level import AccessLevel


class UserSchemaAdd(BaseSchema):
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel | None = None


class UserSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    user_name: str
    first_name: str | None = None
    last_name: str | None = None
    chat_id: int | None = None
    access_level: AccessLevel
    # orders: list[OrderSchema]

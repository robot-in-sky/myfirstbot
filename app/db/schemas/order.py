from pydantic import ConfigDict

from .base import BaseSchema
from app.db.types.order_status import OrderStatus


class OrderSchemaAdd(BaseSchema):
    user_id: int
    first_name: str
    last_name: str
    age: int


class OrderSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    first_name: str
    last_name: str
    age: int
    status: OrderStatus



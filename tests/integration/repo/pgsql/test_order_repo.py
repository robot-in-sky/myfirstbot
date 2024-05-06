import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.entities.order import Order, OrderCreate
from myfirstbot.exceptions import UniqueViolationError
from myfirstbot.repo import OrderRepo


@pytest.fixture()
def order_repo(session: AsyncSession) -> OrderRepo:
    return OrderRepo(session)


@pytest.fixture()
def new_order() -> OrderCreate:
    return OrderCreate(
        user_id=3,
        first_name="John",
        last_name="Doe",
        age=33
    )


class TestOrder:

    async def test_order_add(self, order_repo: OrderRepo, new_order: OrderCreate) -> None:
        result = await order_repo.add(new_order)
        assert isinstance(result, Order)

        # with pytest.raises(UniqueViolationError):
        #     await order_repo.add(new_order)

import pytest

from myfirstbot.db import Database
from myfirstbot.db.exceptions import UniqueViolationError
from myfirstbot.entities.user import User, UserCreate


@pytest.fixture()
def new_user():
    return UserCreate(
        telegram_id=987654321,
        user_name="Cuckold1488",
        first_name="Жмых",
        last_name="Пожилой",
        chat_id=123456789
    )


class TestUser:

    async def test_user_add(self, db: Database, new_user: UserCreate):
        result = await db.user.add(new_user)
        assert isinstance(result, User)

        with pytest.raises(UniqueViolationError):
            await db.user.add(new_user)

        # result = await db.user.get(1)
        # print(result)

        # result = await db.user.get_orders(1)
        # for order in result.orders:
        #     print(order)

        # result = await db.user.get_one(user_id=123458)
        # print(result)

        # result = await db.user.get_one(user_id=000000)
        # print(result)

        # result = await db.user.get_many(chat_id=654321)
        # print(result)

        # result = await db.user.get_many(chat_id=000000)
        # print(result)

        # result = await db.order.add(OrderSchemaAdd(
        #     first_name='Пётр',
        #     last_name='Задов',
        #     age=32,
        #     user_id=1
        # ))
        # print(result)
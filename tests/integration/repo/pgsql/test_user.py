import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from myfirstbot.base.entities.filters import NumQueryFilter
from myfirstbot.entities.enums.access_level import AccessLevel
from myfirstbot.entities.user import User, UserCreate
from myfirstbot.exceptions import UniqueViolationError
from myfirstbot.repo.pgsql.user import UserRepo

import logging

logger = logging.getLogger(__name__)


@pytest.fixture()
def user_repo(session: AsyncSession) -> UserRepo:
    return UserRepo(session)


@pytest.fixture()
def new_user() -> UserCreate:
    return UserCreate(
        telegram_id=987654324,
        user_name="Cuckold1488",
        first_name="Жмых",
        last_name="Пожилой",
        chat_id=123456789,
    )


class TestUser:
    # async def test_user_get(self, user_repo: UserRepo) -> None:
    #     result = await user_repo.get(3)
    #     assert isinstance(result, User)

    async def test_user_get_one(self, user_repo: UserRepo) -> None:
        result = await user_repo.get_one(
            NumQueryFilter(type="eq", field="telegram_id", value=987654324)
        )
        logger.info(result)
        assert isinstance(result, User)

    # async def test_user_add(self, user_repo: UserRepo, new_user: UserCreate) -> None:
    #     result = await user_repo.add(new_user)
    #     logger.warning(result)
    #     assert isinstance(result, User)

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

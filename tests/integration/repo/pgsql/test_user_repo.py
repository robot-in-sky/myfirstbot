import logging
from collections.abc import Sequence

import pytest
import pytest_asyncio

import myfirstbot.base.entities.query as _query
from myfirstbot.entities.user import User, UserCreate
from myfirstbot.exceptions import UniqueViolationError
from myfirstbot.repo.pgsql.user import UserRepo
from tests.utils.mocked_database import MockedDatabase

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(autouse=True, scope="module")
async def _module_setup(database: MockedDatabase) -> None:
    await database.clear()


@pytest_asyncio.fixture()
async def repo(database: MockedDatabase) -> UserRepo:
    async with database.get_session() as _session:
        yield UserRepo(_session)


class TestUserRepo:

    @pytest.mark.parametrize("user", [
        UserCreate(
            telegram_id=123456001,
            user_name="Ivan Ivanov",
            first_name="Ivan",
            last_name="Ivanov",
            chat_id=123456789,
        ),
        UserCreate(
            telegram_id=123456002,
            user_name="Ivan Petrov",
            first_name="Ivan",
            last_name="Petrov",
            chat_id=123456788,
        ),
        UserCreate(
            telegram_id=123456003,
            user_name="priora-king777",
            first_name="Georgio",
            chat_id=123456787,
        ),
        UserCreate(
            telegram_id=123456004,
            user_name="jess69",
            first_name="Sasha",
            chat_id=123456786,
        ),
        UserCreate(
            telegram_id=123456005,
            user_name="raj3456.bangalore",
            first_name="Rajesh",
            last_name="Koothrappali",
        ),
    ])
    async def test_add_and_get(self, repo: UserRepo, user: UserCreate) -> None:
        result = await repo.add(user)
        assert isinstance(result, User)
        result = await repo.get(result.id)
        assert isinstance(result, User)


    async def test_unique_violation(self, repo: UserRepo) -> None:
        with pytest.raises(UniqueViolationError):
            await repo.add(UserCreate(
                telegram_id=123456001,
                user_name="Non-unique User",
            ))


    @pytest.mark.parametrize("id_", [
        -1, 0, int("0x7fffffff", 16),
    ])
    async def test_not_exists(self, repo: UserRepo, id_: int) -> None:
        result = await repo.get(id_)
        assert result is None


    async def test_get_by_telegram_id(self, repo: UserRepo) -> None:
        result = await repo.get_by_telegram_id(123456001)
        assert isinstance(result, User)
        result = await repo.get_by_telegram_id(999999999)
        assert result is None

    @pytest.mark.parametrize(("filters","count"), [
        (None, 5),

        ([_query.NumQueryFilter(type="eq", field="telegram_id", value=123456003)], 1),
        ([_query.NumQueryFilter(type="ne", field="telegram_id", value=123456003)], 4),
        ([_query.NumQueryFilter(type="gt", field="telegram_id", value=123456003)], 2),
        ([_query.NumQueryFilter(type="lt", field="telegram_id", value=123456003)], 2),
        ([_query.NumQueryFilter(type="ge", field="telegram_id", value=123456003)], 3),
        ([_query.NumQueryFilter(type="le", field="telegram_id", value=123456003)], 3),

        ([_query.NullQueryFilter(type="isn", field="chat_id")], 1),
        ([_query.NullQueryFilter(type="isnn", field="chat_id")], 4),

        ([_query.StrQueryFilter(type="eq", field="first_name", value="Ivan")], 2),
        ([_query.StrQueryFilter(type="ne", field="first_name", value="Ivan")], 3),
        ([_query.StrQueryFilter(type="like", field="user_name", value="Ivan")], 2),

        ([_query.SetQueryFilter(
            type="in", field="first_name", value={"Ivan", "Sasha", "John"},
        )], 3),
        ([_query.SetQueryFilter(
            type="nin", field="first_name", value={"Ivan", "Sasha", "John"},
        )], 2),

        ([
             _query.StrQueryFilter(type="eq", field="first_name", value="Ivan"),
             _query.StrQueryFilter(type="eq", field="second_name", value="Ivanov"),
         ], 1),

        (_query.FilterGroup(
            filters=[
                _query.StrQueryFilter(type="eq", field="first_name", value="Rajesh"),
                _query.StrQueryFilter(type="eq", field="first_name", value="Sasha"),
                _query.StrQueryFilter(type="eq", field="first_name", value="Georgio"),
            ],
            join_type="or",
        ), 3),
    ])
    async def test_filters(
            self,
            repo: UserRepo,
            filters: Sequence[_query.QueryFilter] | _query.FilterGroup | None,
            count: int,
    ) -> None:
        result = await repo.get_many(filters=filters)
        assert isinstance(result, list)
        if len(result) > 0:
            for item in result:
                assert isinstance(item, User)
        assert len(result) == count




"""
        (_query.FilterGroup(
            filters=[
                _query.FilterGroup(
                    filters=[
                        _query.StrQueryFilter(type="eq", field="first_name", value="Ivan"),
                        _query.StrQueryFilter(type="eq", field="second_name", value="Sasha"),
                    ],
                    join_type="or",
                ),
                _query.StrQueryFilter(type="eq", field="second_name", value="Petrov"),
            ],
            join_type="and",
        ), 1),
"""


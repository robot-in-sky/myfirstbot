import logging

import pytest
import pytest_asyncio

import myfirstbot.base.entities.query as _query
from myfirstbot.entities.enums.access_level import AccessLevel
from myfirstbot.entities.user import User, UserCreate, UserUpdate
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
            user_name="racer777",
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
            access_level=AccessLevel.AGENT,
        ),
    ])
    async def test_add_and_get(self, repo: UserRepo, user: UserCreate) -> None:
        result = await repo.add(user)
        assert isinstance(result, User)
        assert isinstance(await repo.get(result.id), User)


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
        assert await repo.get(id_) is None


    async def test_get_by_telegram_id(self, repo: UserRepo) -> None:
        result = await repo.get_by_telegram_id(123456001)
        assert isinstance(result, User)
        result = await repo.get_by_telegram_id(999999999)
        assert result is None


    @pytest.mark.parametrize(("args", "expecting"), [
        ({}, 5),
        ({"filters": []}, 5),

        ({"filters": [_query.NumQueryFilter(type="eq", field="telegram_id", value=123456003)]}, 1),
        ({"filters": [_query.NumQueryFilter(type="ne", field="telegram_id", value=123456003)]}, 4),
        ({"filters": [_query.NumQueryFilter(type="gt", field="telegram_id", value=123456003)]}, 2),
        ({"filters": [_query.NumQueryFilter(type="lt", field="telegram_id", value=123456003)]}, 2),
        ({"filters": [_query.NumQueryFilter(type="ge", field="telegram_id", value=123456003)]}, 3),
        ({"filters": [_query.NumQueryFilter(type="le", field="telegram_id", value=123456003)]}, 3),

        ({"filters": [_query.NullQueryFilter(type="isn", field="chat_id")]}, 1),
        ({"filters": [_query.NullQueryFilter(type="isnn", field="chat_id")]}, 4),

        ({"filters": [_query.StrQueryFilter(type="eq", field="first_name", value="Ivan")]}, 2),
        ({"filters": [_query.StrQueryFilter(type="ne", field="first_name", value="Ivan")]}, 3),
        ({"filters": [_query.StrQueryFilter(type="like", field="user_name", value="Ivan")]}, 2),

        ({"filters": [
            _query.SetQueryFilter(type="in", field="first_name", value={"Ivan", "Sasha", "John"}),
        ]}, 3),
        ({"filters": [
            _query.SetQueryFilter(type="nin", field="first_name", value={"Ivan", "Sasha", "John"}),
        ]}, 2),

        ({"filters": [
             _query.StrQueryFilter(type="eq", field="first_name", value="Ivan"),
             _query.StrQueryFilter(type="eq", field="last_name", value="Ivanov"),
        ]}, 1),

        ({"filters": [
             _query.NumQueryFilter(type="eq", field="telegram_id", value=123456003),
             _query.StrQueryFilter(type="eq", field="first_name", value="Ivan"),
             _query.StrQueryFilter(type="eq", field="last_name", value="Koothrappali"),
        ], "or_": True}, 4),

        ({"pagination": _query.Pagination(page=1, page_size=2)}, 2),
        ({"pagination": _query.Pagination(page=2, page_size=2)}, 2),
        ({"pagination": _query.Pagination(page=3, page_size=2)}, 1),
    ])
    async def test_filters_and_pagination(
            self, repo: UserRepo, args: dict, expecting: int,
    ) -> None:
        result = await repo.get_many(**args)
        assert isinstance(result, list)
        if len(result) > 0:
            for item in result:
                assert isinstance(item, User)
        assert len(result) == expecting


    @pytest.mark.parametrize(("args", "expecting"), [
        ({"sorting": _query.Sorting(order_by="telegram_id")},
            (123456001, 123456005)),
        ({"sorting": _query.Sorting(order_by="telegram_id", sort="desc")},
            (123456005, 123456001)),
        ({"sorting": _query.Sorting(order_by="chat_id")},
            (123456786, None)),
        ({"sorting": _query.Sorting(order_by="chat_id", sort="desc")},
            (None, 123456786)),
        ({"sorting": _query.Sorting(order_by="user_name")},
            ("Ivan Ivanov", "raj3456.bangalore")),
        ({"sorting": _query.Sorting(order_by="user_name", sort="desc")},
            ("raj3456.bangalore", "Ivan Ivanov")),
    ])
    async def test_sorting(self, repo: UserRepo, args: dict, expecting: tuple) -> None:
        result = await repo.get_many(**args)
        sorting: _query.Sorting = args["sorting"]
        field = sorting.order_by
        assert getattr(result[0], field) == expecting[0]
        assert getattr(result[-1], field) == expecting[1]

    async def test_update(self, repo: UserRepo) -> None:
        id_ = (await repo.get_many())[0].id
        update = UserUpdate(
            user_name="Agent Smith",
            first_name="Agent",
            last_name="Smith",
            chat_id=888888888,
            access_level=AccessLevel.AGENT,
        )
        result = await repo.update(id_, update)
        for field in update.model_fields:
            assert getattr(result, field) == getattr(update, field)
        updated = await repo.get(id_)
        for field in update.model_fields:
            assert getattr(updated, field) == getattr(update, field)
        assert await repo.update(-1, update) is None


    async def test_delete(self, repo: UserRepo) -> None:
        initial_data = await repo.get_many()
        id_ = initial_data[0].id
        result = await repo.delete(id_)
        assert result == id_
        final_data = await repo.get_many()
        assert len(initial_data) - len(final_data) == 1
        assert await repo.delete(-1) is None

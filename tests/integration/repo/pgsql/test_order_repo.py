import logging
from datetime import UTC, datetime

import pytest
import pytest_asyncio

import myfirstbot.base.entities.query as _query
from myfirstbot.entities.enums.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderCreate, OrderUpdate
from myfirstbot.entities.user import User, UserCreate
from myfirstbot.exceptions import ForeignKeyViolationError
from myfirstbot.repo.pgsql.order import OrderRepo
from myfirstbot.repo.pgsql.user import UserRepo
from tests.utils.mocked_database import MockedDatabase

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(autouse=True, scope="module")
async def _module_setup(database: MockedDatabase) -> None:
    await database.clear()


@pytest_asyncio.fixture(scope="module")
async def user(database: MockedDatabase) -> User:
    async with database.get_session() as _session:
        yield await UserRepo(_session).add(
            UserCreate(telegram_id=123456001, user_name="john_doe"),
        )


@pytest_asyncio.fixture()
async def repo(database: MockedDatabase) -> OrderRepo:
    async with database.get_session() as _session:
        yield OrderRepo(_session)



class TestOrderRepo:

    @pytest.mark.parametrize("order", [
        OrderCreate(
            user_id=-1,
            label="Metallica",
            size=36,
            qty=5,
        ),
        OrderCreate(
            user_id=-1,
            label="Metallica",
            size=38,
            qty=10,
        ),
        OrderCreate(
            user_id=-1,
            label="FSociety",
            size=46,
            qty=1,
        ),
        OrderCreate(
            user_id=-1,
            label="Bharat",
            size=42,
            qty=200,
        ),
        OrderCreate(
            user_id=-1,
            label="Tiger",
            size=48,
            qty=50,
        ),
    ])
    async def test_add_and_get(
            self, repo: OrderRepo, order: OrderCreate, user: User,
    ) -> None:
        order.user_id = user.id
        result = await repo.add(order)
        assert isinstance(result, Order)
        assert isinstance(await repo.get(result.id), Order)


    async def test_foreign_key_violation(self, repo: OrderRepo) -> None:
        with pytest.raises(ForeignKeyViolationError):
            await repo.add(OrderCreate(
                user_id=-1,
                label="Bharat",
                size=32,
                qty=200,
            ))


    @pytest.mark.parametrize("id_", [
        -1, 0, int("0x7fffffff", 16),
    ])
    async def test_not_exists(self, repo: OrderRepo, id_: int) -> None:
        assert await repo.get(id_) is None


    async def test_get_by_user_id(self, repo: OrderRepo, user: User) -> None:
        result = await repo.get_by_user_id(user.id)
        assert isinstance(result, Order)
        result = await repo.get_by_user_id(-1)
        assert result is None


    @pytest.mark.parametrize(("args", "expecting"), [
        ({}, 5),
        ({"filters": []}, 5),

        ({"filters": [_query.NumQueryFilter(type="eq", field="qty", value=10)]}, 1),
        ({"filters": [_query.NumQueryFilter(type="ne", field="qty", value=10)]}, 4),
        ({"filters": [_query.NumQueryFilter(type="gt", field="qty", value=10)]}, 2),
        ({"filters": [_query.NumQueryFilter(type="lt", field="qty", value=10)]}, 2),
        ({"filters": [_query.NumQueryFilter(type="ge", field="qty", value=10)]}, 3),
        ({"filters": [_query.NumQueryFilter(type="le", field="qty", value=10)]}, 3),

        ({"filters": [_query.StrQueryFilter(type="eq", field="label", value="Metallica")]}, 2),
        ({"filters": [_query.StrQueryFilter(type="ne", field="label", value="Metallica")]}, 3),
        ({"filters": [_query.StrQueryFilter(type="like", field="label", value="Metal")]}, 2),

        ({"filters": [
            _query.DateTimeQueryFilter(type="lt", field="created", value=datetime.now(UTC)),
        ]}, 5),
        ({"filters": [
            _query.DateTimeQueryFilter(type="gt", field="created", value=datetime.now(UTC)),
        ]}, 0),

        ({"filters": [
            _query.SetQueryFilter(type="in", field="label", value={"Metallica", "Bharat", "Nirvana"}),
        ]}, 3),
        ({"filters": [
            _query.SetQueryFilter(type="nin", field="label", value={"Metallica", "Bharat", "Nirvana"}),
        ]}, 2),

        ({"pagination": _query.Pagination(page=1, page_size=2)}, 2),
        ({"pagination": _query.Pagination(page=2, page_size=2)}, 2),
        ({"pagination": _query.Pagination(page=3, page_size=2)}, 1),
    ])
    async def test_filters_and_pagination(
            self, repo: OrderRepo, args: dict, expecting: int,
    ) -> None:
        result = await repo.get_many(**args)
        assert isinstance(result, list)
        if len(result) > 0:
            for item in result:
                assert isinstance(item, Order)
        assert len(result) == expecting


    @pytest.mark.parametrize(("args", "expecting"), [
        ({"sorting": _query.Sorting(order_by="size")},
            (36, 48)),
        ({"sorting": _query.Sorting(order_by="size", sort="desc")},
            (48, 36)),
        ({"sorting": _query.Sorting(order_by="label")},
            ("Bharat", "Tiger")),
        ({"sorting": _query.Sorting(order_by="label", sort="desc")},
            ("Tiger", "Bharat")),
    ])
    async def test_sorting(self, repo: OrderRepo, args: dict, expecting: tuple) -> None:
        result = await repo.get_many(**args)
        sorting: _query.Sorting = args["sorting"]
        field = sorting.order_by
        assert getattr(result[0], field) == expecting[0]
        assert getattr(result[-1], field) == expecting[1]


    async def test_update(self, repo: OrderRepo) -> None:
        id_ = (await repo.get_many())[0].id
        update = OrderUpdate(
            label="Foo",
            size=123,
            qty=123,
            status=OrderStatus.PENDING,
        )
        result = await repo.update(id_, update)
        for field in update.model_fields:
            assert getattr(result, field) == getattr(update, field)
        updated = await repo.get(id_)
        for field in update.model_fields:
            assert getattr(updated, field) == getattr(update, field)
        assert await repo.update(-1, update) is None


    async def test_delete(self, repo: OrderRepo) -> None:
        initial_data = await repo.get_many()
        id_ = initial_data[0].id
        result = await repo.delete(id_)
        assert result == id_
        final_data = await repo.get_many()
        assert len(initial_data) - len(final_data) == 1
        assert await repo.delete(-1) is None

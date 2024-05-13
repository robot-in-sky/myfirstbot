import logging
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
import pytz

import myfirstbot.base.entities.query as _query
from myfirstbot.entities.choices.order_status import OrderStatus
from myfirstbot.entities.order import Order, OrderAdd, OrderUpdate
from myfirstbot.entities.user import User, UserAdd
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
    return await UserRepo(database).add(
        UserAdd(telegram_id=123456001, user_name="john_doe"),
    )


@pytest_asyncio.fixture()
async def repo(database: MockedDatabase) -> OrderRepo:
    return OrderRepo(database)



class TestOrderRepo:

    @pytest.mark.parametrize("order", [
        OrderAdd(
            user_id=-1,
            label="Metallica",
            size=36,
            qty=5,
        ),
        OrderAdd(
            user_id=-1,
            label="Metallica",
            size=38,
            qty=10,
        ),
        OrderAdd(
            user_id=-1,
            label="FSociety",
            size=46,
            qty=1,
        ),
        OrderAdd(
            user_id=-1,
            label="Bharat",
            size=42,
            qty=200,
        ),
        OrderAdd(
            user_id=-1,
            label="Tiger",
            size=48,
            qty=50,
        ),
    ])
    async def test_add_and_get(
            self, repo: OrderRepo, order: OrderAdd, user: User,
    ) -> None:
        order.user_id = user.id
        result = await repo.add(order)
        assert isinstance(result, Order)
        assert isinstance(await repo.get(result.id), Order)


    async def test_foreign_key_violation(self, repo: OrderRepo) -> None:
        with pytest.raises(ForeignKeyViolationError):
            await repo.add(OrderAdd(
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


    async def test_set_status(self, repo: OrderRepo) -> None:
        id_ = (await repo.get_many())[0].id
        await repo.set_status(id_, OrderStatus.PENDING)
        status = (await repo.get(id_)).status
        assert status == OrderStatus.PENDING


    @pytest.mark.parametrize(("args", "expecting"), [
        ({}, 5),
        ({"filters": []}, 5),

        ({"filters": [_query.NumQueryFilter(field="qty", type="eq", value=10)]}, 1),
        ({"filters": [_query.NumQueryFilter(field="qty", type="ne", value=10)]}, 4),
        ({"filters": [_query.NumQueryFilter(field="qty", type="gt", value=10)]}, 2),
        ({"filters": [_query.NumQueryFilter(field="qty", type="lt", value=10)]}, 2),
        ({"filters": [_query.NumQueryFilter(field="qty", type="ge", value=10)]}, 3),
        ({"filters": [_query.NumQueryFilter(field="qty", type="le", value=10)]}, 3),

        ({"filters": [_query.StrQueryFilter(field="label", type="eq", value="Metallica")]}, 2),
        ({"filters": [_query.StrQueryFilter(field="label", type="ne", value="Metallica")]}, 3),
        ({"filters": [_query.StrQueryFilter(field="label", type="like", value="Metal")]}, 2),

        ({"filters": [
            _query.DateTimeQueryFilter(field="created", type="lt", value=datetime.now(UTC) + timedelta(minutes=1)),
        ]}, 5),
        ({"filters": [
            _query.DateTimeQueryFilter(field="created", type="gt", value=datetime.now(UTC) + timedelta(minutes=1)),
        ]}, 0),
        ({"filters": [
            _query.DateTimeQueryFilter(
                field="created", type="lt", value=datetime.now(pytz.timezone("Asia/Kolkata")) + timedelta(minutes=1),
            ),
        ]}, 5),
        ({"filters": [
            _query.DateTimeQueryFilter(
                field="created", type="lt", value=datetime.now(pytz.timezone("US/Eastern")) + timedelta(minutes=1),
            ),
        ]}, 5),

        ({"filters": [
            _query.InSetQueryFilter(field="label", type="in", value={"Metallica", "Bharat", "Nirvana"}),
        ]}, 3),
        ({"filters": [
            _query.InSetQueryFilter(field="label", type="nin", value={"Metallica", "Bharat", "Nirvana"}),
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
        )
        result = await repo.update(id_, update)
        for field in update.model_fields:
            assert getattr(result, field) == getattr(update, field)
        updated = await repo.get(id_)
        for field in update.model_fields:
            assert getattr(updated, field) == getattr(update, field)
        assert await repo.update(-1, update) is None


    async def test_delete(self, repo: OrderRepo) -> None:
        initial = await repo.get_many()
        id_ = initial[0].id
        result = await repo.delete(id_)
        assert result == id_
        final = await repo.get_many()
        assert len(initial) - len(final) == 1
        assert await repo.delete(-1) is None


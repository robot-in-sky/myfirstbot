import logging

import pytest
import pytest_asyncio
from src.entities.visa.choices import OrderStatus
from src.entities.order.order import Order, OrderAdd, OrderQueryPaged, OrderUpdate
from src.entities.user.user import User, UserAdd
from src.exceptions import ForeignKeyViolationError
from src.repositories import OrderRepo, UserRepo

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
            label="Metal core",
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
        id_ = (await repo.get_many(OrderQueryPaged())).items[0].id
        await repo.set_status(id_, OrderStatus.PENDING)
        status = (await repo.get(id_)).status
        assert status == OrderStatus.PENDING


    @pytest.mark.parametrize(("query", "expecting"), [
        (OrderQueryPaged(), 5),

        (OrderQueryPaged(status=OrderStatus.DRAFT), 4),
        (OrderQueryPaged(status=OrderStatus.PENDING), 1),
        (OrderQueryPaged(status=OrderStatus.ACCEPTED), 0),

        (OrderQueryPaged(status__in=set()), 0),
        (OrderQueryPaged(status__in={OrderStatus.DRAFT, OrderStatus.ACCEPTED}), 4),
        (OrderQueryPaged(status__in={OrderStatus.PENDING, OrderStatus.ACCEPTED}), 1),
        (OrderQueryPaged(status__in={OrderStatus.DRAFT, OrderStatus.PENDING}), 5),
        (OrderQueryPaged(status__in={OrderStatus.ACCEPTED, OrderStatus.TRASH}), 0),

        (OrderQueryPaged(search="Metal"), 2),
        (OrderQueryPaged(search="Bharat"), 1),
        (OrderQueryPaged(search="a"), 3),
        (OrderQueryPaged(search="i"), 3),

        (OrderQueryPaged(status=OrderStatus.DRAFT, search="Metal"), 1),
        (OrderQueryPaged(status__in={OrderStatus.DRAFT, OrderStatus.PENDING}, search="Metal"), 2),
    ])
    async def test_filters(
            self, repo: OrderRepo, query: OrderQueryPaged, expecting: int,
    ) -> None:
        items = (await repo.get_many(query)).items
        assert isinstance(items, list)
        if len(items) > 0:
            for item in items:
                assert isinstance(item, Order)
        assert len(items) == expecting


    @pytest.mark.parametrize(("query", "expecting"), [
        (OrderQueryPaged(page=1, per_page=2), (1, 2, 3, 2, 5)),
        (OrderQueryPaged(page=2, per_page=2), (2, 2, 3, 2, 5)),
        (OrderQueryPaged(page=3, per_page=2), (3, 2, 3, 1, 5)),
        (OrderQueryPaged(page=1, per_page=3), (1, 3, 2, 3, 5)),
        (OrderQueryPaged(page=2, per_page=3), (2, 3, 2, 2, 5)),
        (OrderQueryPaged(), (1, 10, 1, 5, 5)),
        (OrderQueryPaged(page=1), (1, 10, 1, 5, 5)),
        (OrderQueryPaged(page=100), (100, 10, 1, 0, 5)),
        (OrderQueryPaged(page=-1), (None, None, None, 0, 5)),
        (OrderQueryPaged(per_page=-1), (None, None, None, 0, 5)),
        (OrderQueryPaged(page=1, per_page=-1), (None, None, None, 0, 5)),
        (OrderQueryPaged(page=100, per_page=-1), (None, None, None, 0, 5)),
    ])
    async def test_pagination(
            self, repo: OrderRepo, query: OrderQueryPaged, expecting: tuple,
    ) -> None:
        result = await repo.get_many(query)
        assert result.page == expecting[0]
        assert result.per_page == expecting[1]
        assert result.total_pages == expecting[2]
        assert len(result.items) == expecting[3]
        assert result.total_items == expecting[4]


    @pytest.mark.parametrize(("query", "expecting"), [
        (OrderQueryPaged(sort_by="size"), (36, 48)),
        (OrderQueryPaged(sort_by="size", sort="desc"), (48, 36)),
        (OrderQueryPaged(sort_by="label"), ("Bharat", "Tiger")),
        (OrderQueryPaged(sort_by="label", sort="desc"), ("Tiger", "Bharat")),
    ])
    async def test_sorting(self, repo: OrderRepo, query: OrderQueryPaged, expecting: tuple) -> None:
        items = (await repo.get_many(query)).items
        assert getattr(items[0], query.sort_by) == expecting[0]
        assert getattr(items[-1], query.sort_by) == expecting[1]


    async def test_update(self, repo: OrderRepo) -> None:
        id_ = (await repo.get_many(OrderQueryPaged())).items[0].id
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
        initial = await repo.get_many(OrderQueryPaged())
        id_ = initial.items[0].id
        result = await repo.delete(id_)
        assert result == id_
        final = await repo.get_many(OrderQueryPaged())
        assert len(initial.items) - len(final.items) == 1
        assert await repo.delete(-1) is None

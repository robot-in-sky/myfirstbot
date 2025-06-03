import logging
import uuid

import pytest
import pytest_asyncio

from clients.database import DatabaseClient
from core.entities.users import User, UserAdd, UserQueryPaged, UserRole, UserUpdate
from core.exceptions import UniqueViolationError
from core.orm_models import OrmBase
from core.repositories import UserRepo

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(autouse=True, scope="module")
async def _module_setup(db: DatabaseClient) -> None:
    await db.add_uuid_extension()
    await db.drop_tables_by_base(OrmBase)
    await db.create_tables_by_base(OrmBase)


@pytest_asyncio.fixture()
async def repo(db: DatabaseClient) -> UserRepo:
    return UserRepo(db)


class TestUserRepo:

    @pytest.mark.parametrize("user", [
        UserAdd(
            telegram_id=123456001,
            user_name="Ivan Ivanov",
            first_name="Ivan",
            last_name="Ivanov",
        ),
        UserAdd(
            telegram_id=123456002,
            user_name="Ivan Petrov",
            first_name="Ivan",
            last_name="Petrov",
        ),
        UserAdd(
            telegram_id=123456003,
            user_name="racer777",
            first_name="Georgio",
        ),
        UserAdd(
            telegram_id=123456004,
            user_name="jess69",
            first_name="Sasha",
        ),
        UserAdd(
            telegram_id=123456005,
            user_name="raj3456.bangalore",
            first_name="Rajesh",
            last_name="Koothrappali",
        ),
    ])
    async def test_add_and_get(self, repo: UserRepo, user: UserAdd) -> None:
        result = await repo.add(user)
        assert isinstance(result, User)
        assert isinstance(await repo.get(result.id), User)


    async def test_unique_violation(self, repo: UserRepo) -> None:
        with pytest.raises(UniqueViolationError):
            await repo.add(UserAdd(
                telegram_id=123456001,
                user_name="Non-unique User",
            ))


    async def test_not_exists(self, repo: UserRepo) -> None:
        assert await repo.get(uuid.uuid4()) is None


    async def test_get_by_telegram_id(self, repo: UserRepo) -> None:
        result = await repo.get_by_telegram_id(123456001)
        assert isinstance(result, User)
        result = await repo.get_by_telegram_id(999999999)
        assert result is None


    async def test_set_role(self, repo: UserRepo) -> None:
        # ID of first added item
        id_ = (await repo.get_many(UserQueryPaged(sort="asc"))).items[0].id
        await repo.set_role(id_, UserRole.AGENT)
        role = (await repo.get(id_)).role
        assert role == UserRole.AGENT


    @pytest.mark.parametrize(("query", "expecting"), [
        (UserQueryPaged(), 5),

        (UserQueryPaged(role=UserRole.USER), 4),
        (UserQueryPaged(role=UserRole.AGENT), 1),
        (UserQueryPaged(role=UserRole.ADMINISTRATOR), 0),

        (UserQueryPaged(role__in=set()), 0),
        (UserQueryPaged(role__in={UserRole.USER, UserRole.ADMINISTRATOR}), 4),
        (UserQueryPaged(role__in={UserRole.AGENT, UserRole.ADMINISTRATOR}), 1),
        (UserQueryPaged(role__in={UserRole.USER, UserRole.AGENT}), 5),
        (UserQueryPaged(role__in={UserRole.ADMINISTRATOR, UserRole.BLOCKED}), 0),

        (UserQueryPaged(search="Ivan"), 2),
        (UserQueryPaged(search="je"), 2),
        (UserQueryPaged(search="777"), 1),
        (UserQueryPaged(search="Koothrappali"), 1),

        (UserQueryPaged(role=UserRole.USER, search="Ivan"), 1),
        (UserQueryPaged(role__in={UserRole.USER, UserRole.AGENT}, search="Ivan"), 2),
    ])
    async def test_filters(
            self, repo: UserRepo, query: UserQueryPaged, expecting: int,
    ) -> None:
        items = (await repo.get_many(query)).items
        assert isinstance(items, list)
        if len(items) > 0:
            for item in items:
                assert isinstance(item, User)
        assert len(items) == expecting


    @pytest.mark.parametrize(("query", "expecting"), [
        (UserQueryPaged(page=1, per_page=2), (1, 2, 3, 2, 5)),
        (UserQueryPaged(page=2, per_page=2), (2, 2, 3, 2, 5)),
        (UserQueryPaged(page=3, per_page=2), (3, 2, 3, 1, 5)),
        (UserQueryPaged(page=1, per_page=3), (1, 3, 2, 3, 5)),
        (UserQueryPaged(page=2, per_page=3), (2, 3, 2, 2, 5)),
        (UserQueryPaged(), (1, 10, 1, 5, 5)),
        (UserQueryPaged(page=1), (1, 10, 1, 5, 5)),
        (UserQueryPaged(page=100), (100, 10, 1, 0, 5)),
        (UserQueryPaged(page=-1), (None, None, None, 0, 5)),
        (UserQueryPaged(per_page=-1), (None, None, None, 0, 5)),
        (UserQueryPaged(page=1, per_page=-1), (None, None, None, 0, 5)),
        (UserQueryPaged(page=100, per_page=-1), (None, None, None, 0, 5)),
    ])
    async def test_pagination(
            self, repo: UserRepo, query: UserQueryPaged, expecting: tuple,
    ) -> None:
        result = await repo.get_many(query)
        assert result.page == expecting[0]
        assert result.per_page == expecting[1]
        assert result.total_pages == expecting[2]
        assert len(result.items) == expecting[3]
        assert result.total_items == expecting[4]


    @pytest.mark.parametrize(("query", "expecting"), [
        (UserQueryPaged(sort_by="telegram_id"), (123456005, 123456001)),
        (UserQueryPaged(sort_by="telegram_id", sort="asc"), (123456001, 123456005)),
        (UserQueryPaged(sort_by="telegram_id", sort="desc"), (123456005, 123456001)),
        (UserQueryPaged(sort_by="user_name"), ("raj3456.bangalore", "Ivan Ivanov")),
        (UserQueryPaged(sort_by="user_name", sort="asc"), ("Ivan Ivanov", "raj3456.bangalore")),
        (UserQueryPaged(sort_by="user_name", sort="desc"), ("raj3456.bangalore", "Ivan Ivanov")),
        (UserQueryPaged(sort_by="role"), (UserRole.AGENT, UserRole.USER)),
        (UserQueryPaged(sort_by="role", sort="asc"), (UserRole.USER, UserRole.AGENT)),
    ])
    async def test_sorting(self, repo: UserRepo, query: UserQueryPaged, expecting: tuple) -> None:
        items = (await repo.get_many(query)).items
        assert getattr(items[0], query.sort_by) == expecting[0]
        assert getattr(items[-1], query.sort_by) == expecting[1]


    async def test_update(self, repo: UserRepo) -> None:
        id_ = (await repo.get_many(UserQueryPaged(sort="asc"))).items[0].id
        update = UserUpdate(
            user_name="Foo Bar",
            first_name="Foo",
            last_name="Bar",
            active=False,
        )
        result = await repo.update(id_, update)
        # Check result model fields
        for field in update.model_fields:
            assert getattr(result, field) == getattr(update, field)
        # Check re-requested model fields
        updated = await repo.get(id_)
        for field in update.model_fields:
            assert getattr(updated, field) == getattr(update, field)
        # Update non-existent
        assert await repo.update(uuid.uuid4(), update) is None


    async def test_delete(self, repo: UserRepo) -> None:
        initial = await repo.get_many(UserQueryPaged(sort="asc"))
        id_ = initial.items[0].id
        result = await repo.delete(id_)
        # Result should be ID
        assert result == id_
        final = await repo.get_many(UserQueryPaged())
        assert len(initial.items) - len(final.items) == 1
        # Delete non-existent
        assert await repo.delete(uuid.uuid4()) is None

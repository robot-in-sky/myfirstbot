import logging
import uuid

import pytest
import pytest_asyncio

from clients.database import DatabaseClient
from core.entities.users.user import User, UserAdd
from core.entities.visas import AppForm, AppFormAdd, AppFormQueryPaged, AppFormStatus, AppFormUpdate, Country
from core.exceptions import ForeignKeyViolationError
from core.orm_models import OrmBase
from core.repositories import AppFormRepo, UserRepo

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(autouse=True, scope="module")
async def _module_setup(db: DatabaseClient) -> None:
    await db.add_uuid_extension()
    await db.drop_tables_by_base(OrmBase)
    await db.create_tables_by_base(OrmBase)


@pytest_asyncio.fixture(scope="module")
async def user(db: DatabaseClient) -> User:
    return await UserRepo(db).add(
        UserAdd(telegram_id=123456001, user_name="john_doe"),
    )


@pytest_asyncio.fixture()
async def repo(db: DatabaseClient) -> AppFormRepo:
    return AppFormRepo(db)



class TestAppFormRepo:

    @pytest.mark.parametrize("params", [
        {
            "country": Country.IND,
            "visa_id": "id1",
            "data": {"name": "Ivan Ivanov"},
            "given_name": "Ivan",
            "surname": "Ivanov",
        },
        {
            "country": Country.IND,
            "visa_id": "id2",
            "data": {"name": "Ivan Petrov"},
            "given_name": "Ivan",
            "surname": "Petrov",
        },
        {
            "country": Country.VNM,
            "visa_id": "id2",
            "data": {"name": "Georgio"},
            "given_name": "Georgio",
        },
        {
            "country": Country.VNM,
            "visa_id": "id3",
            "data": {"name": "Sasha"},
        },
        {
            "country": Country.RUS,
            "visa_id": "id3",
            "data": {"name": "Rajesh Koothrappali"},
        },
    ])
    async def test_add_and_get(
            self, repo: AppFormRepo, params: dict, user: User,
    ) -> None:
        result = await repo.add(AppFormAdd(user_id=user.id, **params))
        assert isinstance(result, AppForm)
        assert isinstance(await repo.get(result.id), AppForm)


    async def test_foreign_key_violation(self, repo: AppFormRepo) -> None:
        with pytest.raises(ForeignKeyViolationError):
            await repo.add(AppFormAdd(
                country=Country.RUS,
                visa_id="id1",
                data={},
                user_id=uuid.uuid4(),
            ))


    async def test_not_exists(self, repo: AppFormRepo) -> None:
        assert await repo.get(uuid.uuid4()) is None


    async def test_set_status(self, repo: AppFormRepo) -> None:
        # ID of first added item
        id_ = (await repo.get_many(AppFormQueryPaged(sort="asc"))).items[0].id
        await repo.set_status(id_, AppFormStatus.PENDING)
        status = (await repo.get(id_)).status
        assert status == AppFormStatus.PENDING


    @pytest.mark.parametrize(("query", "expecting"), [
        (AppFormQueryPaged(), 5),

        (AppFormQueryPaged(status=AppFormStatus.DRAFT), 4),
        (AppFormQueryPaged(status=AppFormStatus.PENDING), 1),
        (AppFormQueryPaged(status=AppFormStatus.ACCEPTED), 0),

        (AppFormQueryPaged(status__in=set()), 0),
        (AppFormQueryPaged(status__in={AppFormStatus.DRAFT, AppFormStatus.ACCEPTED}), 4),
        (AppFormQueryPaged(status__in={AppFormStatus.PENDING, AppFormStatus.ACCEPTED}), 1),
        (AppFormQueryPaged(status__in={AppFormStatus.DRAFT, AppFormStatus.PENDING}), 5),
        (AppFormQueryPaged(status__in={AppFormStatus.ACCEPTED, AppFormStatus.TRASH}), 0),
        (AppFormQueryPaged(status__not_in={AppFormStatus.PENDING, AppFormStatus.TRASH}), 4),

        (AppFormQueryPaged(country=Country.IND), 2),
        (AppFormQueryPaged(country=Country.VNM), 2),
        (AppFormQueryPaged(country=Country.RUS), 1),

        (AppFormQueryPaged(country__in=set()), 0),
        (AppFormQueryPaged(country__in={Country.IND, Country.VNM}), 4),
        (AppFormQueryPaged(country__in={Country.IND, Country.RUS}), 3),
        (AppFormQueryPaged(country__in={Country.IND, Country.THA}), 2),
        (AppFormQueryPaged(country__in={Country.THA, Country.USA}), 0),
    ])
    async def test_filters(
            self, repo: AppFormRepo, query: AppFormQueryPaged, expecting: int,
    ) -> None:
        items = (await repo.get_many(query)).items
        assert isinstance(items, list)
        if len(items) > 0:
            for item in items:
                assert isinstance(item, AppForm)
        assert len(items) == expecting


    @pytest.mark.parametrize(("query", "expecting"), [
        (AppFormQueryPaged(page=1, per_page=2), (1, 2, 3, 2, 5)),
        (AppFormQueryPaged(page=2, per_page=2), (2, 2, 3, 2, 5)),
        (AppFormQueryPaged(page=3, per_page=2), (3, 2, 3, 1, 5)),
        (AppFormQueryPaged(page=1, per_page=3), (1, 3, 2, 3, 5)),
        (AppFormQueryPaged(page=2, per_page=3), (2, 3, 2, 2, 5)),
        (AppFormQueryPaged(), (1, 10, 1, 5, 5)),
        (AppFormQueryPaged(page=1), (1, 10, 1, 5, 5)),
        (AppFormQueryPaged(page=100), (100, 10, 1, 0, 5)),
        (AppFormQueryPaged(page=-1), (None, None, None, 0, 5)),
        (AppFormQueryPaged(per_page=-1), (None, None, None, 0, 5)),
        (AppFormQueryPaged(page=1, per_page=-1), (None, None, None, 0, 5)),
        (AppFormQueryPaged(page=100, per_page=-1), (None, None, None, 0, 5)),
    ])
    async def test_pagination(
            self, repo: AppFormRepo, query: AppFormQueryPaged, expecting: tuple,
    ) -> None:
        result = await repo.get_many(query)
        assert result.page == expecting[0]
        assert result.per_page == expecting[1]
        assert result.total_pages == expecting[2]
        assert len(result.items) == expecting[3]
        assert result.total_items == expecting[4]


    async def test_update(self, repo: AppFormRepo) -> None:
        id_ = (await repo.get_many(AppFormQueryPaged(sort="asc"))).items[0].id
        update = AppFormUpdate(
            data={"surname": "Kumar"}
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


    async def test_delete(self, repo: AppFormRepo) -> None:
        initial = await repo.get_many(AppFormQueryPaged(sort="asc"))
        id_ = initial.items[0].id
        # Result should be ID
        result = await repo.delete(id_)
        assert result == id_
        final = await repo.get_many(AppFormQueryPaged(sort="asc"))
        assert len(initial.items) - len(final.items) == 1
        # Delete non-existent
        assert await repo.delete(uuid.uuid4()) is None

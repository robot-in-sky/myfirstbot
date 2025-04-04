import logging
from uuid import UUID

from src.entities.base import QueryCountItem, QueryResult
from src.entities.users import User, UserRole
from src.entities.visas import AppForm, AppFormAdd, AppFormQuery, AppFormQueryPaged, AppFormStatus, AppFormUpdate
from src.exceptions import AccessDeniedError, InvalidStateError, NotFoundError
from src.infrastructure.database import DatabaseClient
from src.repositories import AppFormRepo
from src.services.public.visa_service import VisaService
from src.services.utils.access_level import access_level


class MyAppFormsService:

    def __init__(self, db: DatabaseClient, current_user: User) -> None:
        self._app_form_repo = AppFormRepo(db)
        self._visa_service = VisaService()
        self.current_user = current_user

    def _log(self, app_form: AppForm, message: str) -> None:
        logging.info(f"AppForm #{app_form.id} [@{self.current_user.user_name}]: {message}")


    async def get_my_forms(self, q: AppFormQueryPaged) -> QueryResult[AppForm]:
        q.user_id = self.current_user.id
        q.status__not_in = q.status__not_in or set()
        q.status__not_in.add(AppFormStatus.TRASH)
        return await self._app_form_repo.get_many(q)


    async def get_my_forms_count(self, q: AppFormQuery) -> int:
        q.user_id = self.current_user.id
        q.status__not_in = q.status__not_in or set()
        q.status__not_in.add(AppFormStatus.TRASH)
        return await self._app_form_repo.get_count(q)


    async def get_my_forms_count_by_status(self, q: AppFormQuery) -> list[QueryCountItem[AppFormStatus]]:
        q.user_id = self.current_user.id
        q.status__not_in = q.status__not_in or set()
        q.status__not_in.add(AppFormStatus.TRASH)
        return await self._app_form_repo.get_count_by_status(q)


    @access_level(required=UserRole.USER)
    async def new_form(self, instance: AppFormAdd) -> AppForm:
        app_form = await self._app_form_repo.add(instance)
        app_form.visa = self._visa_service.get_visa(app_form.visa_id)
        self._log(app_form, "created")
        return app_form


    def _check_ownership(self, app_form: AppForm) -> None:
        if (self.current_user.role == UserRole.USER and
                app_form.user_id != self.current_user.id):
            raise AccessDeniedError


    @staticmethod
    def _check_status(app_form: AppForm, status__in: list[AppFormStatus]) -> None:
        if app_form.status not in status__in:
            raise InvalidStateError


    async def get_form(self, id_: UUID) -> AppForm:
        if app_form := await self._app_form_repo.get(id_):
            app_form.visa = self._visa_service.get_visa(app_form.visa_id)
            self._check_ownership(app_form)
            return app_form
        raise NotFoundError


    @access_level(required=UserRole.USER)
    async def update_form(self, id_: UUID, instance: AppFormUpdate) -> AppForm:
        if app_form := await self._app_form_repo.update(id_, instance):
            app_form.visa = self._visa_service.get_visa(app_form.visa_id)
            self._check_ownership(app_form)
            self._check_status(app_form, [AppFormStatus.DRAFT])
            self._log(app_form, "updated")
            return app_form
        raise NotFoundError


    @access_level(required=UserRole.USER)
    async def save_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_ownership(app_form)
            self._check_status(app_form, [AppFormStatus.DRAFT])
            if await self._app_form_repo.set_status(id_, AppFormStatus.SAVED):
                self._log(app_form, "submitted")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.USER)
    async def submit_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_ownership(app_form)
            self._check_status(app_form, [AppFormStatus.SAVED])
            if await self._app_form_repo.set_status(id_, AppFormStatus.PENDING):
                self._log(app_form, "submitted")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.USER)
    async def return_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_ownership(app_form)
            self._check_status(app_form, [AppFormStatus.PENDING])
            if await self._app_form_repo.set_status(id_, AppFormStatus.DRAFT):
                self._log(app_form, "returned")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.USER)
    async def trash_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_ownership(app_form)
            self._check_status(app_form, [AppFormStatus.DRAFT, AppFormStatus.SAVED])
            if await self._app_form_repo.set_status(id_, AppFormStatus.TRASH):
                self._log(app_form, "trashed")
                return app_form.id
        raise NotFoundError

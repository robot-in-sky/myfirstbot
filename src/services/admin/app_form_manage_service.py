import logging
from uuid import UUID

from src.entities.base import QueryCountItem, QueryResult
from src.entities.users import User, UserRole
from src.entities.visas import AppForm, AppFormAdd, AppFormQuery, AppFormQueryPaged, AppFormStatus, AppFormUpdate
from src.exceptions import InvalidStateError, NotFoundError
from src.infrastructure.database import DatabaseClient
from src.repositories.app_form_repo import AppFormRepo
from src.services.public.visa_service import VisaService
from src.services.utils.access_level import access_level


class AppFormManageService:

    def __init__(self, db: DatabaseClient, current_user: User) -> None:
        self._app_form_repo = AppFormRepo(db)
        self._visa_service = VisaService()
        self.current_user = current_user


    def _log(self, app_form: AppForm, message: str) -> None:
        logging.info(f"AppForm #{app_form.id} [@{self.current_user.user_name}]: {message}")


    @access_level(required=UserRole.AGENT)
    async def get_forms(self, q: AppFormQueryPaged) -> QueryResult[AppForm]:
        return await self._app_form_repo.get_many(q)


    @access_level(required=UserRole.AGENT)
    async def get_forms_count(self, q: AppFormQuery) -> int:
        return await self._app_form_repo.get_count(q)


    @access_level(required=UserRole.AGENT)
    async def get_count_by_status(self, q: AppFormQuery) -> list[QueryCountItem[AppFormStatus]]:
        return await self._app_form_repo.get_count_by_status(q)


    @access_level(required=UserRole.AGENT)
    async def new_form(self, instance: AppFormAdd) -> AppForm:
        app_form = await self._app_form_repo.add(instance)
        app_form.visa = self._visa_service.get_visa(app_form.visa_id)
        self._log(app_form, "created")
        return app_form


    @staticmethod
    def _check_status(form: AppForm, status: AppFormStatus) -> None:
        if form.status != status:
            raise InvalidStateError


    @access_level(required=UserRole.AGENT)
    async def get_form(self, id_: UUID) -> AppForm:
        if app_form := await self._app_form_repo.get(id_):
            app_form.visa = self._visa_service.get_visa(app_form.visa_id)
            return app_form
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def update_form(self, id_: UUID, instance: AppFormUpdate) -> AppForm:
        if app_form := await self._app_form_repo.update(id_, instance):
            app_form.visa = self._visa_service.get_visa(app_form.visa_id)
            self._log(app_form, "updated")
            return app_form
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def submit_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.DRAFT)
            if await self._app_form_repo.set_status(id_, AppFormStatus.PENDING):
                self._log(app_form, "submitted")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def return_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.PENDING)
            if await self._app_form_repo.set_status(id_, AppFormStatus.DRAFT):
                self._log(app_form, "returned")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def trash_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.DRAFT)
            if await self._app_form_repo.set_status(id_, AppFormStatus.TRASH):
                self._log(app_form, "trashed")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def accept_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.PENDING)
            if await self._app_form_repo.set_status(id_, AppFormStatus.ACCEPTED):
                self._log(app_form, "accepted")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def reject_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.PENDING)
            if await self._app_form_repo.set_status(id_, AppFormStatus.DRAFT):
                self._log(app_form, "rejected")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def done_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.ACCEPTED)
            if await self._app_form_repo.set_status(id_, AppFormStatus.COMPLETED):
                self._log(app_form, "done")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def restore_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.TRASH)
            if await self._app_form_repo.set_status(id_, AppFormStatus.DRAFT):
                self._log(app_form, "restored")
                return app_form.id
        raise NotFoundError


    @access_level(required=UserRole.AGENT)
    async def delete_form(self, id_: UUID) -> UUID:
        if app_form := await self._app_form_repo.get(id_):
            self._check_status(app_form, AppFormStatus.TRASH)
            if await self._app_form_repo.delete(id_):
                self._log(app_form, "deleted")
                return app_form.id
        raise NotFoundError

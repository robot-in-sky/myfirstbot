from dataclasses import dataclass

from aio_pika.patterns import JsonRPC

from src.entities.users import User
from src.infrastructure.database import DatabaseClient
from src.infrastructure.redis import RedisClient
from src.infrastructure.s3 import S3Client
from src.services import (
    AppFormManageService,
    AttachmentService,
    AuthService,
    FormService,
    MyAppFormsService,
    MyAttachmentsService,
    UserManageService,
    VisaService,
)
from src.settings import AppSettings


@dataclass(frozen=True)
class Dependencies:
    settings: AppSettings
    db: DatabaseClient
    redis: RedisClient
    s3: S3Client
    rpc: JsonRPC

    # Public services
    @staticmethod
    def get_visa_service() -> VisaService:
        return VisaService()

    @staticmethod
    def get_forms_service() -> FormService:
        return FormService()

    def get_auth_service(self) -> AuthService:
        return AuthService(db=self.db)

    def get_my_app_forms_service(self, current_user: User) -> MyAppFormsService:
        return MyAppFormsService(db=self.db, current_user=current_user)

    def get_my_attachments_service(self, current_user: User) -> MyAttachmentsService:
        return MyAttachmentsService(s3=self.s3, db=self.db, current_user=current_user)


    # Admin services
    def get_user_manage_service(self, current_user: User) -> UserManageService:
        return UserManageService(db=self.db, current_user=current_user)

    def get_app_form_manage_service(self, current_user: User) -> AppFormManageService:
        return AppFormManageService(db=self.db, current_user=current_user)

    def get_attachment_service(self, current_user: User) -> AttachmentService:
        return AttachmentService(s3=self.s3, current_user=current_user)

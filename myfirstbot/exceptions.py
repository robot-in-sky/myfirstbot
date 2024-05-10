class AppError(Exception):
    ...


class ValidationError(AppError):
    ...


class ServiceError(AppError):
    ...


class AccessDeniedError(ServiceError):
    ...


class InvalidStateError(ServiceError):
    ...


class RepositoryError(AppError):
    ...


class ForeignKeyViolationError(RepositoryError):
    ...


class UniqueViolationError(RepositoryError):
    ...





class AppError(Exception):
    ...


class ValidationError(AppError):
    ...


class RepositoryError(AppError):
    ...


class ForeignKeyViolationError(RepositoryError):
    ...


class NotNullViolationError(RepositoryError):
    ...


class UniqueViolationError(RepositoryError):
    ...





class AppError(Exception):
    ...


class RepositoryError(AppError):
    ...


class ForeignKeyViolationError(RepositoryError):
    ...


class NotNullViolationError(RepositoryError):
    ...


class UniqueViolationError(RepositoryError):
    ...


class OutputValidationError(RepositoryError):
    ...



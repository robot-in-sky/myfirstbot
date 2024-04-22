class AppError(Exception):
    ...


class RepositoryError(AppError):
    ...


class UniqueViolationError(RepositoryError):
    ...


class ForeignKeyViolationError(RepositoryError):
    ...


class SchemaValidationError(RepositoryError):
    ...


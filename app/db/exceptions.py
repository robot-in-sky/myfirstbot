from app.exceptions import AppException


class RepositoryError(AppException):
    """Base repository error"""


class UniqueViolationError(RepositoryError):
    """Violation of unique constraint"""


class ForeignKeyViolationError(RepositoryError):
    """Violation of foreign key constraint"""


class SchemaValidationError(RepositoryError):
    """Schema validation error"""

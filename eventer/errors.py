class EventerError(Exception):
    """
    Base exception for all eventer related errors
    """
    pass


class EventerValidationError(EventerError):
    """
    An exception that is produced when a validation fails.
    """
    pass


class CategoryValidationError(EventerValidationError):
    pass


class FieldNotFoundError(EventerError):
    pass

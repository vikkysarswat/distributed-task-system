"""Custom exceptions for the task system."""


class TaskSystemException(Exception):
    """Base exception for the task system."""
    pass


class TaskNotFoundError(TaskSystemException):
    """Raised when a task is not found."""
    pass


class TaskValidationError(TaskSystemException):
    """Raised when task validation fails."""
    pass


class ServiceUnavailableError(TaskSystemException):
    """Raised when a service is unavailable."""
    pass


class RateLimitExceededError(TaskSystemException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after


class AuthenticationError(TaskSystemException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(TaskSystemException):
    """Raised when authorization fails."""
    pass


class DatabaseError(TaskSystemException):
    """Raised when database operations fail."""
    pass


class CacheError(TaskSystemException):
    """Raised when cache operations fail."""
    pass
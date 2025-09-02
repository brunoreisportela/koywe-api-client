"""
Custom exceptions for Koywe API client
"""


class KoyweAPIError(Exception):
    """Base exception for all Koywe API errors"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(KoyweAPIError):
    """Raised when authentication fails"""
    pass


class ValidationError(KoyweAPIError):
    """Raised when request validation fails"""
    pass


class NotFoundError(KoyweAPIError):
    """Raised when a resource is not found"""
    pass


class RateLimitError(KoyweAPIError):
    """Raised when API rate limit is exceeded"""
    pass


class NetworkError(KoyweAPIError):
    """Raised when network connectivity issues occur"""
    pass


class ServerError(KoyweAPIError):
    """Raised when server returns 5xx errors"""
    pass


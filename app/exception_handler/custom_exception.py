class AppError(Exception):
    """Base class for application-specific exceptions."""

    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    """Exception for 404 errors."""

    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AppError):
    """Exception for validation errors."""

    def __init__(self, message="Invalid input"):
        super().__init__(message, status_code=422)


class BadRequestError(AppError):
    def __init__(self, message="Invalid input"):
        super().__init__(message, status_code=400)


class InvalidCredential(AppError):
    def __int__(self, message="Invalid Credential"):
        super().__init__(message, status_code=401)


class ProductNotFoundError(AppError):
    def __int__(self, message="Product not found"):
        super().__init__(message, status_code=400)

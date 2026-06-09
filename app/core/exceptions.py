from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class BadRequest(AppException):
    def __init__(self, message: str = 'Bad request'):
        super().__init__(message, 400)


class Unauthorized(AppException):
    def __init__(self, message: str = 'Unauthorized'):
        super().__init__(message, 401)


class Forbidden(AppException):
    def __init__(self, message: str = 'Forbidden'):
        super().__init__(message, 403)


class NotFound(AppException):
    def __init__(self, message: str = 'Resource not found'):
        super().__init__(message, 404)


class Conflict(AppException):
    def __init__(self, message: str = 'Conflict'):
        super().__init__(message, 409)


class InternalServerError(AppException):
    def __init__(self, message: str = 'Internal server error'):
        super().__init__(message, 500)


class Teapot(AppException):
    def __init__(self, message: str = "I'm a teapot"):
        super().__init__(message, 418)


async def app_exception_handler(request: Request, exception: Exception):
    if isinstance(exception, AppException):
        return JSONResponse(
            status_code=exception.status_code,
            content={'detail': exception.message},
        )
    return JSONResponse(
        status_code=500,
        content={'detail': 'Internal Server Error'},
    )
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.libs.exceptions import BaseHTTPException


class AppExceptionHandler:
    """Base application exception handler"""

    def __init__(self, exception: BaseHTTPException):
        self.message = str(exception)
        self.status_code = getattr(
            exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.headers = {}

    def raise_exception(self):
        """Raises the exception with the appropriate status code"""
        message = {
            "status": "failed",
            "message": self.message,
        }
        return JSONResponse(
            status_code=self.status_code, content=message, headers=self.headers
        )


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        try:
            # process the request and get the response
            response = await call_next(request)
            return response
        except Exception as e:
            return AppExceptionHandler(e).raise_exception()

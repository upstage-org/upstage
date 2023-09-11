import sys

import traceback
from typing import Union

from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import Response

class RequestExceptionHandling():

    def __init__(self,logger):
        self.logger = logger

    async def request_validation_exception_handler(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        This is a wrapper to the default RequestValidationException handler of FastAPI.
        This function will be called when client input is not valid.
        """
        #self.logger.error(f"Our custom request_validation_exception_handler was called: {traceback.format_exc()}")
        # loguru shows the stack trace automatically.
        self.logger.exception(f"Our custom request_validation_exception_handler was called")
        body = await request.body()
        query_params = request.query_params._dict  # pylint: disable=protected-access
        detail = {"errors": exc.errors(), "body": body.decode(), "query_params": query_params}
        self.logger.exception(detail)
        return await _request_validation_exception_handler(request, exc)
    
    async def http_exception_handler(self, request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
        """
        This is a wrapper to the default HTTPException handler of FastAPI.
        This function will be called when a HTTPException is explicitly raised.
        """
        #self.logger.error(f"Our custom http_exception_handler was called: {traceback.format_exc()}")
        # loguru shows the stack trace automatically.
        self.logger.exception(f"Our custom http_exception_handler was called")
        return await _http_exception_handler(request, exc)
    
    
    async def unhandled_exception_handler(self, request: Request, exc: Exception) -> PlainTextResponse:
        """
        This middleware will log all unhandled exceptions.
        Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
        """
        host = getattr(getattr(request, "client", None), "host", None)
        port = getattr(getattr(request, "client", None), "port", None)
        url = f"{request.url.path}?{request.query_params}" if request.query_params else request.url.path
        exception_type, exception_value, exception_traceback = sys.exc_info()
        exception_name = getattr(exception_type, "__name__", None)
        #self.logger.error(
        #    f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {traceback.format_exc()}>'
        #)
        # loguru shows the stack trace automatically.
        self.logger.exception(
            f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error'
        )
        return PlainTextResponse(str(exc), status_code=500)


import logging
from fastapi import FastAPI, Request
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from shared.building_blocks import (
    DomainException,
    ApplicationException,
    get_status_code_for_exception,
    CustomHTTPException,
)
from shared.adapters.rest import ErrorResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(
        request: Request, exc: DomainException
    ) -> JSONResponse:
        status_code = get_status_code_for_exception(exc)

        error_response = ErrorResponse(
            error=exc.__class__.__name__, message=exc.message
        )

        logger.warning(
            f"Domain exception: {exc.__class__.__name__} - {exc.message}",
            extra={
                "exception_type": exc.__class__.__name__,
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=status_code, content=error_response.model_dump()
        )

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request, exc: ApplicationException
    ) -> JSONResponse:
        status_code = get_status_code_for_exception(exc)

        error_response = ErrorResponse(
            error=exc.__class__.__name__, message=exc.message
        )

        logger.warning(
            f"Application exception: {exc.__class__.__name__} - {exc.message}",
            extra={
                "exception_type": exc.__class__.__name__,
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=status_code, content=error_response.model_dump()
        )

    @app.exception_handler(CustomHTTPException)
    async def custom_http_exception_handler(
        request: Request, exc: CustomHTTPException
    ) -> JSONResponse:
        error_response = ErrorResponse(error=exc.error, message=exc.message)

        logger.warning(
            f"Custom HTTP exception: {exc.error} - {exc.message}",
            extra={
                "exception_type": exc.error,
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=exc.status_code, content=error_response.model_dump()
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(status_code=422, content=exc.errors())

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        error_response = ErrorResponse(
            error="InternalServerError", message="An unexpected error occurred"
        )

        logger.error(
            f"Unexpected exception: {exc.__class__.__name__} - {str(exc)}",
            exc_info=True,
            extra={
                "exception_type": exc.__class__.__name__,
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(status_code=500, content=error_response.model_dump())

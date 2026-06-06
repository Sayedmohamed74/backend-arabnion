from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from h11 import Request
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
            "data": None,
            "error": exc.detail,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "message": "Validation Error",
            "data": None,
            "error": "Validation Error",
        },
    )


async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "message": "Internal Server Error",
            "data": None,
            "error": str(exc),
        },
    )

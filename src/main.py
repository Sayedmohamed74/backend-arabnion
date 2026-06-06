from fastapi import FastAPI, Request
from src.routes import auth, teacher , student
from fastapi.responses import JSONResponse
from src.utils.wrap_response import success_response

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",
    same_site="lax",
    https_only=False
)
# =========================
# HTTP Exception Handler
# =========================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=success_response(None, exc.detail, exc.status_code , True),
    )


# =========================
# Validation Error Handler
# =========================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=success_response(None, "Validation Error", 422, True),
    )


# =========================
# Global Exception Handler
# =========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=success_response(None, "Internal Server Error", 500, True),
    )


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
app.include_router(student.router, prefix="/student", tags=["student"])

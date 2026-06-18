from fastapi import FastAPI, Request
from src.routes import auth, teacher, student, package, dialects,teacher_dialect
from fastapi.responses import JSONResponse
from src.utils.wrap_response import success_response

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from contextlib import asynccontextmanager
from src.lib.connect_db import db
from src.repositories.users import RepoAdmin
from src.utils.hash import hash_password
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 1. الحصول على الـ generator
#     db_gen = db()

#     # 2. استخراج الـ Session الحقيقي من داخل الـ generator باستخدام anext
#     session = await anext(db_gen)

#     try:
#         # 3. تمرير الـ Session الحقيقي للـ Repository
#         repoAdmin = RepoAdmin(db=session)

#         # 4. تشغيل الكود بنجاح
#         s = await repoAdmin.list_users()
#         if(len(s)!=0):
#             print('uses')
#         else:
#             hass = hash_password('Aa@123')
#             await repoAdmin.create_user({
#                 'email':'admin@admin.com',
#                 'password':hass,
#                 'name':'a'
#             })


#     finally:
#         # 5. تنظيف الجلسة وإغلاق الـ generator بشكل آمن بعد الانتهاء
#         try:
#             await anext(db_gen)
#         except StopAsyncIteration:
#             pass

#     yield

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# HTTP Exception Handler
# =========================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=success_response(None, exc.detail, exc.status_code, True),
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
app.include_router(package.router, prefix="/package", tags=["package"])
app.include_router(dialects.router, prefix="/dialects", tags=["dialects"])
app.include_router(teacher_dialect.router, prefix="/teacher-dialect", tags=["teacher-dialect"])

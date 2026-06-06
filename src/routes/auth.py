from fastapi import APIRouter, Depends, Body, Request, security
from fastapi.exceptions import HTTPException
from src.models.request_model import TeacherCreate, StudentCreate, LoginRequest
from src.models.response_model import ResponseModel
from src.utils.wrap_response import success_response
from src.lib.connect_db import db
from sqlalchemy import text
from typing import Annotated
from src.repositories.users import RepoTeacher, RepoStudent, RepoAdmin
from src.services.user import TeacherService, AdminService, StudentService
from src.utils.hash import hash_password, verify_password
from src.utils.errors import raise_error, ErrorKey
from src.utils.check_pass import is_admin, is_invalid_or_expired_token
from src.lib.jwt import create_access_token, create_refresh_token, decode_token
from src.types.models import EncodeTokenType


router = APIRouter()


@router.post("/register/teacher")
async def register_teacher(
    body: Annotated[TeacherCreate, Body()], db=Depends(db), user=Depends(decode_token)
):
    repo = RepoTeacher(db)
    service = TeacherService(repo)
    is_invalid_or_expired_token(user)
    is_admin(user)
    result = await service.create_teacher(body)

    return True


@router.post("/register/student")
async def register_student(
    body: Annotated[StudentCreate, Body()], db=Depends(db), user=Depends(decode_token)
):
    repo = RepoStudent(db)
    service = StudentService(repo)
    is_invalid_or_expired_token(user)
    is_admin(user)
    result = await service.create_student(body)

    return True


@router.post("/login/student")
async def login_student(request:Request, body: Annotated[LoginRequest, Body()], db=Depends(db)):
    repo = RepoStudent(db)
    service = StudentService(repo)
    ac_token = await service.login_student(body)
   
    return ac_token


@router.post("/login/teacher")
async def login_teacher(body: Annotated[LoginRequest, Body()], db=Depends(db)):
    repo = RepoTeacher(db)
    service = TeacherService(repo)
    ac_token = await service.login_teacher(body)

    return ac_token


@router.post("/login/admin")
async def login_admin(body: Annotated[LoginRequest, Body()], db=Depends(db)):
    repo = RepoAdmin(db)
    service = AdminService(repo)
    ac_token = await service.login_admin(body)
    return ac_token

@router.get("/refresh-token")
async def refresh_token(
    db=Depends(db), user: EncodeTokenType = Depends(decode_token)
):
    is_invalid_or_expired_token(user)
    
    user.pop("exp", None)
    ac_token = create_access_token(user)
    return success_response(
        {
            "access_token": ac_token,
        },
        message="Token refreshed successfully",
    )
    
@router.get("/get-user")
async def get_user(
    db=Depends(db), user: EncodeTokenType = Depends(decode_token)
):
    is_invalid_or_expired_token(user)
    user.pop("exp", None)
    
    return success_response(
        {
            "user": user,
        },
        message="User data retrieved successfully",
        
    )
    
@router.post("/")
async def doc_login(
    form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()], db=Depends(db)
):
    repo = RepoAdmin(db)
    service = AdminService(repo)
    t = LoginRequest(email=form_data.username, password=form_data.password)
    ac_token = await service.login_admin(t)

    return {"access_token": ac_token.access_token, "token_type": "bearer"}

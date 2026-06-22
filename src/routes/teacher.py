from fastapi import APIRouter, Depends, Body, HTTPException, Query, Path
from typing import Annotated
from src.utils.wrap_response import success_response, list_response
from src.lib.connect_db import db
from src.repositories.users import RepoTeacher, RepoStudentForTeacher
from src.repositories.teacher_dialects import RepoTeacherDialect
from src.services.user import TeacherService, StudentForTeacherService
from src.lib.jwt import create_access_token, decode_token
from sqlalchemy import text
from src.models.request_model import FilterParams, FilterParams, UpdateUserModel,FilterTeacherParams ,TeacherUpdate
from src.models.response_model import (
    ResponseModel,
    ResponseModelList,
    ResponseUserModel,
    ResponseTeacherModel,
)
from src.lib.jwt import decode_token
from src.utils.check_pass import is_admin, is_invalid_or_expired_token, is_teacher
from src.utils.errors import raise_error, ErrorKey

router = APIRouter()


@router.get(
    "/list", tags=["teacher"], response_model=ResponseModelList[ResponseUserModel]
)
async def list_teachers(
    pagination: Annotated[FilterTeacherParams, Query()],
    db=Depends(db),
    user=Depends(decode_token),
):
    repo = RepoTeacher(db)
    services = TeacherService(repo)
    is_invalid_or_expired_token(user)
    is_admin(user)
    teachers = await services.get_list(role=user.get("role"), pagination=pagination)
    total = await services.get_total(role=user.get("role"))
    return list_response(
        teachers,
        offset=pagination.offset,
        limit=pagination.limit,
        total=total,
        message="List teachers",
    )


@router.get("/me", response_model=ResponseModel[ResponseTeacherModel])
async def get_me(db=Depends(db), user=Depends(decode_token)):
    is_invalid_or_expired_token(user)
    is_teacher(user)

    repo = RepoTeacher(db)
    service = TeacherService(repo)
    result = await service.get_me(user["id"])

    return result


@router.get("/me/students")
async def get_my_students(
    pagination: Annotated[FilterParams, Query()],
    db=Depends(db),
    user=Depends(decode_token),
):
    repo = RepoStudentForTeacher(db)
    service = StudentForTeacherService(repo)
    is_invalid_or_expired_token(user)
    is_teacher(user)
    students = await service.list_students_for_teacher(
        teacher_id=user["id"], pagination=pagination
    )
    return students


# @router.delete("/me")
# async def delete_me(db=Depends(db), user=Depends(decode_token)):
#     if not is_teacher(user):
#         raise_error(ErrorKey.UNAUTHORIZED, "Only teachers can access this endpoint")
#     repo = RepoTeacher(db)
#     service = TeacherService(repo)
#     result = await service.remove_me(user["id"], role=user["role"])
#     return result


@router.get("/{teacher_id}", response_model=ResponseModel[ResponseTeacherModel])
async def get_teacher(teacher_id: str, db=Depends(db), user=Depends(decode_token)):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoTeacher(db)
    service = TeacherService(repo)
    teacher = await service.get_me(teacher_id)
    if not teacher:
        raise_error(ErrorKey.NOT_FOUND, "Teacher not found")

    return teacher


@router.put("/{teacher_id}", response_model=ResponseModel[ResponseUserModel])
async def update_teacher(
    body: Annotated[TeacherUpdate, Body()],
    teacher_id: Annotated[str, Path()],
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)

    repo = RepoTeacher(db)
    service = TeacherService(repo)
    print('========',body)
    teacher_data = body.model_dump(exclude_unset=True)

    updated_teacher = await service.update_teacher(teacher_id, teacher_data)
    updated_teacher.create_at = updated_teacher.create_at.isoformat()
    if not updated_teacher:
        raise_error(ErrorKey.NOT_FOUND, "Teacher not found")

    return success_response(updated_teacher, message="Teacher updated successfully")


@router.delete("/{teacher_id}")
async def delete_teacher(
    teacher_id: Annotated[str, Path()], db=Depends(db), user=Depends(decode_token)
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoTeacher(db)
    service = TeacherService(repo)
    result = await service.delete_teacher(teacher_id, role=user["role"])
    return result

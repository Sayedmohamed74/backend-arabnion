from fastapi import APIRouter, Depends, Body, HTTPException, Query, Path
from typing import Annotated
from src.utils.wrap_response import success_response, list_response
from src.lib.connect_db import db
from src.repositories.users import RepoTeacher, RepoStudentForTeacher
from src.services.user import TeacherService, StudentForTeacherService
from src.lib.jwt import create_access_token, decode_token
from sqlalchemy import text
from src.models.request_model import FilterParams, FilterParams, UpdateUserModel
from src.models.response_model import ResponseModel, ResponseModelList, ResponseUserModel
from src.lib.jwt import decode_token
from src.utils.check_pass import is_admin, is_invalid_or_expired_token, is_teacher
from src.utils.errors import raise_error, ErrorKey

router = APIRouter()


@router.get("/list", tags=["teacher"], response_model=ResponseModelList[ResponseUserModel])
async def list_teachers(
    pagination: Annotated[FilterParams, Query()],
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


@router.get("/me")
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


@router.get("/{teacher_id}")
async def get_teacher(teacher_id: int, db=Depends(db), user=Depends(decode_token)):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoTeacher(db)
    service = TeacherService(repo)
    teacher = await service.repo.get_user(teacher_id)
    if not teacher:
        raise_error(ErrorKey.NOT_FOUND, "Teacher not found")
    data = {
        "id": teacher.id,
        "name": teacher.name,
        "email": teacher.email,
        "country": teacher.country,
        "telephone": teacher.tel,
        "created_at": teacher.create_at.isoformat(),
    }
    return success_response(data, message="Get teacher details")


@router.put("/{teacher_id}",response_model=ResponseModel[ResponseUserModel])
async def update_teacher(
    body: Annotated[UpdateUserModel, Body()],
    teacher_id: Annotated[int, Path()],
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)

    repo = RepoTeacher(db)
    service = TeacherService(repo)
    teacher_data = body.model_dump(exclude_unset=True)
    

    updated_teacher = await service.update_teacher(teacher_id, teacher_data)
    updated_teacher.create_at = updated_teacher.create_at.isoformat()
    if not updated_teacher:
        raise_error(ErrorKey.NOT_FOUND, "Teacher not found")

    return success_response(updated_teacher, message="Teacher updated successfully")


@router.delete("/{teacher_id}")
async def delete_teacher(
    teacher_id: Annotated[int, Path()], db=Depends(db), user=Depends(decode_token)
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoTeacher(db)
    service = TeacherService(repo)
    result = await service.delete_teacher(teacher_id, role=user["role"])
    return result

from fastapi import APIRouter, Depends, Body, HTTPException, Query, Path
from typing import Annotated
from src.utils.wrap_response import success_response, list_response
from src.utils.check_pass import is_admin, is_invalid_or_expired_token, is_student
from src.lib.connect_db import db
from src.repositories.users import RepoStudent
from src.services.user import StudentService
from src.lib.jwt import decode_token
from src.models.request_model import FilterParams, UpdateUserModel
from src.models.response_model import ResponseModelList, ResponseUserModel


router = APIRouter()


@router.get("/list")
async def list_students(
    pagination: Annotated[FilterParams, Query()],
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoStudent(db)
    services = StudentService(repo)
    students = await services.get_list(role=user.get("role"), pagination=pagination)
    total = await services.get_total(role=user.get("role"))
    data = [
        {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "country": student.country,
            "telephone": student.tel,
            "created_at": student.create_at.isoformat(),
        }
        for student in students
    ]
    return list_response(
        data,
        offset=pagination.offset,
        limit=pagination.limit,
        total=total,
        message="List students",
    )


@router.get("/me")
async def get_student_me(
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_student(user)
    repo = RepoStudent(db)
    services = StudentService(repo)
    student = await services.get_me(id=user.get("id"))
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/{student_id}")
async def get_student_by_id(
    student_id: Annotated[str, Path()],
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoStudent(db)
    services = StudentService(repo)
    student = await services.get_me(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}")
async def update_student(
    student_id: Annotated[str, Path()],
    student_data: Annotated[UpdateUserModel, Body()],
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoStudent(db)
    services = StudentService(repo)
    data = student_data.model_dump(exclude_unset=True)
    updated_student = await services.update_student(
        student_data=data, student_id=student_id
    )
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    print(updated_student.name)
    return success_response(
        {
            "id": updated_student.id,
            "name": updated_student.name,
            "email": updated_student.email,
            "country": updated_student.country,
            "telephone": updated_student.tel,
            "created_at": updated_student.create_at.isoformat(),
        },
        message="Student updated successfully",
    )


@router.delete("/{student_id}")
async def delete_student(
    student_id: Annotated[str, Path()],
    db=Depends(db),
    user=Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoStudent(db)
    services = StudentService(repo)
    result = await services.delete_student(student_id=student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return success_response({}, message="Student deleted successfully")

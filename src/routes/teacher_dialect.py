from fastapi import APIRouter, Depends, Body, HTTPException, Path
from typing import Annotated
from src.utils.wrap_response import success_response
from src.utils.check_pass import is_admin, is_invalid_or_expired_token
from src.lib.connect_db import db
from src.repositories.teacher_dialects import RepoTeacherDialect
from src.lib.jwt import decode_token
from src.models.request_model import TeacherDialectModel
from src.models.response_model import ResponseTeacherDialectModel
from src.types.models import EncodeTokenType


router = APIRouter()


@router.post("/add")
async def add_dialect_to_teacher(
    body: Annotated[TeacherDialectModel, Body()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    """Add a dialect to a teacher - Admin only"""
    is_invalid_or_expired_token(user)
    is_admin(user)
    
    teacher_id = body.teacher_id
    dialect_id = body.dialect_id
    
    if not teacher_id or not dialect_id:
        raise HTTPException(status_code=400, detail="teacher_id and dialect_id required")
    
    repo = RepoTeacherDialect(db)
    
    
    result = await repo.add_dialect_to_teacher(teacher_id, dialect_id)
    return success_response(result, message="Dialect added to teacher successfully")


@router.delete("/{teacher_id}/{dialect_id}")
async def remove_dialect_from_teacher(
    teacher_id: Annotated[str, Path()],
    dialect_id: Annotated[str, Path()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    """Remove a dialect from a teacher - Admin only"""
    is_invalid_or_expired_token(user)
    is_admin(user)
    
    repo = RepoTeacherDialect(db)
    
    result = await repo.remove_dialect_from_teacher(teacher_id, dialect_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Dialect not found for this teacher")
    
    return success_response({}, message="Dialect removed from teacher successfully")




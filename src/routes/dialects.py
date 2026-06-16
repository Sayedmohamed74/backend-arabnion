from fastapi import APIRouter, Depends, Body, HTTPException, Query, Path
from typing import Annotated
from src.utils.wrap_response import success_response, list_response
from src.utils.check_pass import is_admin, is_invalid_or_expired_token
from src.lib.connect_db import db
from src.repositories.dialects import RepoDialect
from src.services.dialects import DialectService
from src.lib.jwt import decode_token
from src.models.request_model import DialectCreate, FilterParams
from src.types.models import EncodeTokenType


router = APIRouter()


@router.get("/list")
async def list_dialects(
    pagination: Annotated[FilterParams, Query()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    repo = RepoDialect(db)
    service = DialectService(repo)
    dialects = await service.list_dialects(
        offset=pagination.offset, limit=pagination.limit, search=pagination.search
    )
    total = len(dialects)
    data = [
        {
            "id": str(dialect.id),
            "name": dialect.name,
        }
        for dialect in dialects
    ]
    return list_response(
        data,
        offset=pagination.offset,
        limit=pagination.limit,
        total=total,
        message="List dialects",
    )


@router.get("/{dialect_id}")
async def get_dialect(
    dialect_id: Annotated[str, Path()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    repo = RepoDialect(db)
    service = DialectService(repo)
    dialect = await service.get_dialect(dialect_id)
    return success_response(
        {
            "id": str(dialect.id),
            "name": dialect.name,
        },
        message="Dialect retrieved successfully",
    )


@router.post("/create")
async def create_dialect(
    dialect_data: Annotated[DialectCreate, Body()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoDialect(db)
    service = DialectService(repo)
    new_dialect = await service.create_dialect(
        role=user.get("role"), dialect_data=dialect_data
    )
    return success_response(
        {
            "id": str(new_dialect.id),
            "name": new_dialect.name,
        },
        message="Dialect created successfully",
    )


@router.put("/{dialect_id}")
async def update_dialect(
    dialect_id: Annotated[str, Path()],
    dialect_data: Annotated[DialectCreate, Body()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoDialect(db)
    service = DialectService(repo)
    updated_dialect = await service.update_dialect(
        role=user.get("role"),
        dialect_id=dialect_id,
        dialect_data=dialect_data.model_dump(exclude_unset=True),
    )
    return success_response(
        {
            "id": str(updated_dialect.id),
            "name": updated_dialect.name,
        },
        message="Dialect updated successfully",
    )


@router.delete("/{dialect_id}")
async def delete_dialect(
    dialect_id: Annotated[str, Path()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoDialect(db)
    service = DialectService(repo)
    await service.delete_dialect(role=user.get("role"), dialect_id=dialect_id)
    return success_response({}, message="Dialect deleted successfully")

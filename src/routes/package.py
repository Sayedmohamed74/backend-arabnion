from fastapi import APIRouter, Depends, Body, HTTPException, Query, Path
from typing import Annotated
from src.utils.wrap_response import success_response, list_response
from src.utils.check_pass import is_admin, is_invalid_or_expired_token
from src.lib.connect_db import db
from src.repositories.package import RepoPackage
from src.services.package import PackageService
from src.lib.jwt import decode_token
from src.models.request_model import PackageCreate, FilterParams
from src.types.models import EncodeTokenType


router = APIRouter()


@router.get("/list")
async def list_packages(
    pagination: Annotated[FilterParams, Query()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    repo = RepoPackage(db)
    service = PackageService(repo)
    packages = await service.list_packages(
        offset=pagination.offset, limit=pagination.limit, search=pagination.search
    )
    total = len(packages)
    data = [
        {
            "id": str(package.id),
            "name": package.name,
            "lesson": package.lesson,
            "monthly_payment": package.mount_paid,
            "features": package.features,
        }
        for package in packages
    ]
    return list_response(
        data,
        offset=pagination.offset,
        limit=pagination.limit,
        total=total,
        message="List packages",
    )


@router.get("/{package_id}")
async def get_package(
    package_id: Annotated[str, Path()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    repo = RepoPackage(db)
    service = PackageService(repo)
    package = await service.get_package(package_id)
    return success_response(
        {
            "id": str(package.id),
            "name": package.name,
            "lesson": package.lesson,
            "monthly_payment": package.mount_paid,
            "features": package.features,
        },
        message="Package retrieved successfully",
    )


@router.post("/create")
async def create_package(
    package_data: Annotated[PackageCreate, Body()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoPackage(db)
    service = PackageService(repo)
    new_package = await service.create_package(
        role=user.get("role"), package_data=package_data
    )
    return success_response(
        {
            "id": str(new_package.id),
            "name": new_package.name,
            "lesson": new_package.lesson,
            "monthly_payment": new_package.mount_paid,
            "features": new_package.features,
        },
        message="Package created successfully",
    )


@router.put("/{package_id}")
async def update_package(
    package_id: Annotated[str, Path()],
    package_data: Annotated[PackageCreate, Body()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoPackage(db)
    service = PackageService(repo)

    # Map request field names to database field names
    mapped_data = package_data.model_dump(exclude_unset=True)

    updated_package = await service.update_package(
        role=user.get("role"), package_id=package_id, package_data=mapped_data
    )
    return success_response(
        {
            "id": str(updated_package.id),
            "name": updated_package.name,
            "lesson": updated_package.lesson,
            "monthly_payment": updated_package.mount_paid,
            "features": updated_package.features,
        },
        message="Package updated successfully",
    )


@router.delete("/{package_id}")
async def delete_package(
    package_id: Annotated[str, Path()],
    db=Depends(db),
    user: EncodeTokenType = Depends(decode_token),
):
    is_invalid_or_expired_token(user)
    is_admin(user)
    repo = RepoPackage(db)
    service = PackageService(repo)
    result = await service.delete_package(role=user.get("role"), package_id=package_id)
    return success_response({}, message="Package deleted successfully")

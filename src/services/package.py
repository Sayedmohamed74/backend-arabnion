from fastapi import HTTPException

from src.repositories.package import RepoPackage
from src.types.models import PackageType
from src.models.request_model import PackageCreate, FilterParams
from src.utils.errors import raise_error, ErrorKey
from src.utils.wrap_response import success_response


class PackageService:
    def __init__(self, repo: RepoPackage):
        self.repo = repo

    async def create_package(self, role: str, package_data: PackageCreate):
        """Only admin can create packages"""
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        data: PackageType = {
            "name": package_data.name,
            "lesson": package_data.lesson,
            "mount_paid": package_data.mount_paid,
            "features": package_data.features,
        }
        return await self.repo.create_package(data)

    async def list_packages(self, offset=0, limit=10, search=None):
        return await self.repo.list_packages(offset, limit, search)

    async def get_package(self, package_id: str):
        package = await self.repo.get_package(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        return package

    async def update_package(self, role: str, package_id: str, package_data: dict):
        """Only admin can update packages"""
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        package = await self.repo.get_package(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")

        return await self.repo.update_package(package_id, package_data)

    async def delete_package(self, role: str, package_id: str):
        """Only admin can delete packages"""
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        package = await self.repo.get_package(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")

        return await self.repo.delete_package(package_id)

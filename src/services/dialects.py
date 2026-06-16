from fastapi import HTTPException

from src.repositories.dialects import RepoDialect
from src.types.models import DialectType
from src.models.request_model import DialectCreate
from src.utils.errors import raise_error, ErrorKey
from src.utils.wrap_response import success_response


class DialectService:
    def __init__(self, repo: RepoDialect):
        self.repo = repo

    async def create_dialect(self, role: str, dialect_data: DialectCreate):
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        data: DialectType = {
            "name": dialect_data.name,
        }
        return await self.repo.create_dialect(data)

    async def list_dialects(self, offset=0, limit=10, search=None):
        return await self.repo.list_dialects(offset, limit, search)

    async def get_dialect(self, dialect_id: str):
        dialect = await self.repo.get_dialect(dialect_id)
        if not dialect:
            raise HTTPException(status_code=404, detail="Dialect not found")
        return dialect

    async def update_dialect(self, role: str, dialect_id: str, dialect_data: dict):
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        dialect = await self.repo.get_dialect(dialect_id)
        if not dialect:
            raise HTTPException(status_code=404, detail="Dialect not found")

        return await self.repo.update_dialect(dialect_id, dialect_data)

    async def delete_dialect(self, role: str, dialect_id: str):
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        dialect = await self.repo.get_dialect(dialect_id)
        if not dialect:
            raise HTTPException(status_code=404, detail="Dialect not found")

        return await self.repo.delete_dialect(dialect_id)

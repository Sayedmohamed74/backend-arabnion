from sqlalchemy import select, update

from src.models.model_db import Package
from src.repositories.db import RepoDB


class RepoPackage(RepoDB):
    model = Package

    async def get_package(self, key):
        result = await self.db.execute(select(self.model).where(self.model.id == key))
        return result.scalar_one_or_none()

    async def list_packages(self, offset=0, limit=10, search=None):
        query = select(self.model).order_by(self.model.id)

        if search:
            query = query.where(self.model.name.contains(search))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_package(self, data):
        new_package = self.model(**data)
        self.db.add(new_package)
        await self.db.commit()
        await self.db.refresh(new_package)
        return new_package

    async def update_package(self, key, data):
        await self.db.execute(
            update(self.model).where(self.model.id == key).values(**data)
        )
        await self.db.commit()
        return await self.get_package(key)

    async def delete_package(self, key):
        package = await self.get_package(key)
        if not package:
            return None

        await self.db.delete(package)
        await self.db.commit()
        return package

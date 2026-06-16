from sqlalchemy import select, update

from src.models.model_db import Dialects
from src.repositories.db import RepoDB


class RepoDialect(RepoDB):
    model = Dialects

    async def get_dialect(self, key):
        result = await self.db.execute(select(self.model).where(self.model.id == key))
        return result.scalar_one_or_none()

    async def list_dialects(self, offset=0, limit=10, search=None):
        query = select(self.model).order_by(self.model.id)

        if search:
            query = query.where(self.model.name.contains(search))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_dialect(self, data):
        new_dialect = self.model(**data)
        self.db.add(new_dialect)
        await self.db.commit()
        await self.db.refresh(new_dialect)
        return new_dialect

    async def update_dialect(self, key, data):
        await self.db.execute(
            update(self.model).where(self.model.id == key).values(**data)
        )
        await self.db.commit()
        return await self.get_dialect(key)

    async def delete_dialect(self, key):
        dialect = await self.get_dialect(key)
        if not dialect:
            return None

        await self.db.delete(dialect)
        await self.db.commit()
        return dialect

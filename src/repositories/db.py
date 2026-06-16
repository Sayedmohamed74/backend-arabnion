from sqlalchemy.ext.asyncio import AsyncSession


class RepoDB:
    def __init__(self, db: AsyncSession):
        self.db = db

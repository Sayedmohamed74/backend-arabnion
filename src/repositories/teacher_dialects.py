from sqlalchemy import select, insert, delete
import uuid
from src.models.model_db import Teacher, Dialects, TeacherDialect
from src.repositories.db import RepoDB


class RepoTeacherDialect(RepoDB):
    async def add_dialect_to_teacher(
        self, teacher_id: str, dialect_ids: list[uuid.UUID]
    ):
        """Add a dialect to a teacher"""
        values = [
            {"teacher_id": teacher_id, "dialect_id": dialect_id}
            for dialect_id in dialect_ids
        ]
        stmt = insert(TeacherDialect).values(values)
        await self.db.execute(stmt)
        await self.db.commit()
        return True

    async def remove_dialect_from_teacher(self, teacher_id: str, dialect_id: str):
        """Remove a dialect from a teacher"""
        stmt = delete(TeacherDialect).where(
            (TeacherDialect.teacher_id == teacher_id)
            & (TeacherDialect.dialect_id == dialect_id)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def geTeacherDialect(self, teacher_id: str):
        """Get all dialects for a specific teacher"""
        stmt = (
            select(Dialects)
            .join(TeacherDialect, TeacherDialect.dialect_id == Dialects.id)
            .where(TeacherDialect.teacher_id == teacher_id)
        )

        result = await self.db.execute(stmt)
        print(result)
        return result.scalars().all()

    async def get_dialects_teachers(self, dialect_id: str):
        """Get all teachers for a specific dialect"""
        stmt = (
            select(Teacher)
            .join(TeacherDialect, TeacherDialect.teacher_id == Teacher.id)
            .where(TeacherDialect.id == dialect_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def teacher_has_dialect(self, teacher_id: str, dialect_id: str) -> bool:
        """Check if a teacher has a specific dialect"""
        stmt = select(TeacherDialect).where(
            (TeacherDialect.teacher_id == teacher_id)
            & (TeacherDialect.dialect_id == dialect_id)
        )
        result = await self.db.execute(stmt)
        return result.first() is not None

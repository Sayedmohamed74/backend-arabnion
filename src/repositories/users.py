from abc import ABC, abstractmethod

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.model_db import Student, Teacher, Admin ,Dialects
from typing import Generic, TypeVar
from src.utils.wrap_response import list_response
from src.models.response_model import ResponseModelList, ResponseUserModel

T = TypeVar("T")


class RepoDB:
    def __init__(self, db: AsyncSession):
        self.db = db


class RepoUser(ABC):
    @abstractmethod
    async def get_user(self, key):
        pass

    @abstractmethod
    async def get_user_by_email(self, email):
        pass

    @abstractmethod
    async def list_users(self, offset=0, limit=10):
        pass

    @abstractmethod
    async def delete_user(self, key):
        pass

    @abstractmethod
    async def update_user(self, key, data):
        pass

    @abstractmethod
    async def create_user(self, data):
        pass


class BaseRepo(RepoDB, RepoUser, Generic[T]):
    model: type[T] = None

    async def get_user(self, key):
        result = await self.db.execute(select(self.model).where(self.model.id == key))

        return result.scalar_one_or_none()

    async def get_user_by_email(self, email):
        result = await self.db.execute(
            select(self.model).where(self.model.email == email)
        )

        return result.scalar_one_or_none()

    async def list_users(self, offset=0, limit=10, search=None, country=None, tel=None):
        query = (
            select(self.model)
            .offset(offset)
            .limit(limit)
            .order_by(self.model.create_at.desc())  # يفضل الترتيب حسب الأحدث
        )
        if search:
            query = query.where(
                self.model.name.contains(search) | self.model.email.contains(search)
            )
        if country:
            query = query.where(self.model.country == country)
        if tel:
            query = query.where(self.model.tel == tel)

        result = await self.db.execute(query)

        return result.scalars().all()

    async def delete_user(self, key):
        user = await self.get_user(key)
        print('========',user.__dict__)

        if not user:
            return None

        await self.db.delete(user)
        await self.db.commit()

        return user

    async def update_user(self, key, data):
        print('=================',data)
        await self.db.execute(
            update(self.model).where(self.model.id == key).values(**data)
        )

        await self.db.commit()

        return await self.get_user(key)

    async def create_user(self, data):
        new_user = self.model(**data)

        self.db.add(new_user)

        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user


class RepoStudent(BaseRepo[Student]):
    model = Student

    async def get_user(self, key):
        result = await self.db.execute(
            select(Student)
            .options(
                selectinload(Student.teacher),
                selectinload(Student.package),
                selectinload(Student.dialect),
                selectinload(Student.countries),
            )
            .where(Student.id == key)
        )

        return result.scalar_one_or_none()
    async def list_users(self, offset=0, limit=10, search=None, country=None, tel=None):
        query = (
            select(self.model).options(selectinload(Student.countries))
            .offset(offset)
            .limit(limit)
            .order_by(self.model.create_at.desc())  # يفضل الترتيب حسب الأحدث
        )
        if search:
            query = query.where(
                self.model.name.contains(search) | self.model.email.contains(search)
            )
        if country:
            query = query.where(self.model.country == country)
        if tel:
            query = query.where(self.model.tel == tel)

        result = await self.db.execute(query)

        return result.scalars().all()


class RepoTeacher(BaseRepo[Teacher]):
    model = Teacher

    async def list_users(self, offset=0, limit=10, search=None, country=None, tel=None, dialect=None):
        query = (
        select(Teacher)
        .options(selectinload(Teacher.dialect))
        .order_by(Teacher.create_at.desc())
    )
        if search:
            query = query.where(
                Teacher.name.contains(search) |
                Teacher.email.contains(search)
            )
    
        if country:
            query = query.where(Teacher.country == country)
    
        if tel:
            query = query.where(Teacher.tel == tel)
    
        if dialect:
            query = query.where(
            Teacher.dialect.any(Dialects.id.in_(dialect))
            )
    
        result = await self.db.execute(query)
    
        return result.scalars().all()

    async def get_user(self, key):
        result = await self.db.execute(
            select(Teacher)
            .options(
                selectinload(Teacher.dialect),
                selectinload(Teacher.countries),
                
            )
            .where(Teacher.id == key)
        )

        return result.scalar_one_or_none()


class RepoAdmin(BaseRepo[Admin]):
    model = Admin


class RepoStudentForTeacher(RepoDB):
    async def list_students_for_teacher(
        self, teacher_id: int, offset=0, limit=10
    ) -> ResponseModelList[ResponseUserModel]:
        total_result = await self.db.execute(
            select(func.count(Student.id)).where(Student.teacher_id == teacher_id)
        )
        result = await self.db.execute(
            select(Student)
            .where(Student.teacher_id == teacher_id)
            .offset(offset)
            .limit(limit)
        )
        total = total_result.scalar()
        data = result.scalars().all()
        mapped_data = [
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "country": student.country,
                "telephone": student.tel,
                "created_at": student.create_at.isoformat(),
            }
            for student in data
        ]

        return list_response(
            mapped_data,
            offset=offset,
            limit=limit,
            total=total,
            message="List students for teacher",
        )

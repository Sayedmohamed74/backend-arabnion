from fastapi import HTTPException
from sqlalchemy import func, select, text

from src.repositories.users import (
    RepoStudent,
    RepoTeacher,
    RepoAdmin,
    RepoStudentForTeacher,
)
from src.types.models import TeacherType, AdminType, PackageType, StudentType
from src.models.request_model import (
    AdminCreate,
    LoginRequest,
    StudentCreate,
    TeacherCreate,
    FilterParams,
)
from src.models.response_model import ResponseTokenModel , ResponseModel
from src.utils.hash import hash_password, verify_password
from src.lib.jwt import create_access_token, create_refresh_token
from src.utils.errors import raise_error, ErrorKey
from src.utils.wrap_response import success_response


class StudentService:
    def __init__(self, repo: RepoStudent):
        self.repo = repo

    async def login_student(self, student: LoginRequest) -> ResponseTokenModel:
        user = await self.repo.get_user_by_email(student.email)
        if not user:
            raise HTTPException(status_code=403, detail="UnAuth")
        if not verify_password(student.password, user.password):
            raise HTTPException(status_code=403, detail="UnAuth")

        ac_token = create_access_token(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "country": user.country,
                "phone": user.tel,
                "role": "student",
            }
        )
        re_token = create_refresh_token(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "country": user.country,
                "phone": user.tel,
                "role": "student",
            }
        )
        return ResponseModel(status=200, message="Login successful", data=ResponseTokenModel(access_token=ac_token, refresh_token=re_token))

    async def create_student(self, student_data: StudentCreate):

        student = await self.repo.get_user_by_email(student_data.email)

        if student:
            raise HTTPException(status_code=400, detail="Email already exists")

        hash_pass = hash_password(student_data.password)
        data: TeacherType = {
            "country": student_data.country,
            "email": student_data.email,
            "name": student_data.name,
            "password": hash_pass,
            "tel": student_data.phone,
        }
        return await self.repo.create_user(data)

    async def update_student(self, student_id: int, student_data: dict):

        student = await self.repo.get_user(student_id)

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return await self.repo.update_user(student_id, student_data)

    async def delete_student(self, student_id: int):

        student = await self.repo.get_user(student_id)

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return await self.repo.delete_user(student_id)
    async def get_list(self, role: str, pagination: FilterParams):
        if not role == "admin":
            raise_error(ErrorKey.FORBIDDEN)
        return await self.repo.list_users(pagination.offset, pagination.limit ,search=pagination.search, country=pagination.country, tel=pagination.tel)
    
    async def get_total(self, role: str):
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        stmt = select(func.count(self.repo.model.id))

        result = await self.repo.db.execute(stmt)
        return result.scalar()

    
    async def get_me(self, id: int):

        user = await self.repo.get_user(id)
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "country": user.country,
            "telephone": user.tel,
            "created_at": user.create_at.isoformat(),
        }
        return success_response(data)



class TeacherService:
    def __init__(self, repo: RepoTeacher):
        self.repo = repo

    async def login_teacher(self, teacher: LoginRequest) -> ResponseTokenModel:
        user = await self.repo.get_user_by_email(teacher.email)
        if not user:
            raise HTTPException(status_code=403, detail="UnAuth")
        if not verify_password(teacher.password, user.password):
            raise HTTPException(status_code=403, detail="UnAuth")

        ac_token = create_access_token(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "country": user.country,
                "phone": user.tel,
                "role": "teacher",
            }
        )
        re_token = create_refresh_token(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "country": user.country,
                "phone": user.tel,
                "role": "teacher",
            }
        )
        return ResponseModel(status=200, message="Login successful", data=ResponseTokenModel(access_token=ac_token, refresh_token=re_token))

    async def create_teacher(self, teacher_data: TeacherCreate):

        teacher = await self.repo.get_user_by_email(teacher_data.email)

        if teacher:
            raise HTTPException(status_code=400, detail="Email already exists")
        hash_pass = hash_password(teacher_data.password)
        data: TeacherType = {
            "country": teacher_data.country,
            "email": teacher_data.email,
            "name": teacher_data.name,
            "password": hash_pass,
            "tel": teacher_data.phone,
        }

        return await self.repo.create_user(data)

    async def update_teacher(self, teacher_id: int, teacher_data: dict):

        teacher = await self.repo.get_user(teacher_id)

        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return await self.repo.update_user(teacher_id, teacher_data)

    async def get_total(self, role: str):
        if role != "admin":
            raise_error(ErrorKey.FORBIDDEN)

        stmt = select(func.count(self.repo.model.id))

        result = await self.repo.db.execute(stmt)
        return result.scalar()

    async def get_list(self, role: str, pagination: FilterParams):
        if not role == "admin":
            raise_error(ErrorKey.FORBIDDEN)
        return await self.repo.list_users(pagination.offset, pagination.limit , search=pagination.search, country=pagination.country, tel=pagination.tel)

    async def get_me(self, id: int):

        user = await self.repo.get_user(id)
        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "country": user.country,
            "telephone": user.tel,
            "created_at": user.create_at.isoformat(),
        }
        return success_response(data)

    async def remove_me(self, id: int, role):
        if not role == "teacher":
            raise_error(ErrorKey.FORBIDDEN)
        user = await self.repo.delete_user(id)
        return success_response(user)

    async def delete_teacher(self, teacher_id: int, role: str):
        if not role == "admin":
            raise_error(ErrorKey.FORBIDDEN)
        teacher = await self.repo.get_user(teacher_id)

        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        return await self.repo.delete_user(teacher_id)


class AdminService:
    def __init__(self, repo: RepoAdmin):
        self.repo = repo

    async def login_admin(self, admin: LoginRequest) -> ResponseTokenModel:
        user = await self.repo.get_user_by_email(admin.email)
        if not user:
            raise HTTPException(status_code=403, detail="UnAuth")
        if not verify_password(admin.password, user.password):
            raise HTTPException(status_code=403, detail="UnAuth")

        ac_token = create_access_token(
            {"id": user.id, "email": user.email, "name": user.name, "role": "admin"}
        )
        re_token = create_refresh_token(
            {"id": user.id, "email": user.email, "name": user.name, "role": "admin"}
        )
        return ResponseModel(status=200, message="Login successful", data=ResponseTokenModel(access_token=ac_token, refresh_token=re_token))

    async def create_admin(self, admin_data: dict):

        admin = await self.repo.get_user_by_email(admin_data["email"])

        if admin:
            raise HTTPException(status_code=400, detail="Email already exists")

        return await self.repo.create_user(admin_data)

    async def update_admin(self, admin_id: int, admin_data: dict):

        admin = await self.repo.get_user(admin_id)

        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        return await self.repo.update_user(admin_id, admin_data)

    async def delete_admin(self, admin_id: int):

        admin = await self.repo.get_user(admin_id)

        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        return await self.repo.delete_user(admin_id)


class StudentForTeacherService:
    def __init__(self, repo: RepoStudentForTeacher):
        self.repo = repo

    async def list_students_for_teacher(
        self, teacher_id: int, pagination: FilterParams
    ):
        return await self.repo.list_students_for_teacher(
            teacher_id, pagination.offset, pagination.limit
        )

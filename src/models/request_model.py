import re
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_phone_value(cls, v):
    pattern = r"^\+?[1-9]\d{7,14}$"
    if not re.match(pattern, v):
        raise ValueError("Invalid phone number format")
    return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUserModel(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    tel: Optional[str] = Field(default=None, validation_alias="phone")

    @field_validator("tel")
    def validate_phone(cls, v):
        if v is not None:
            return validate_phone_value(cls, v)
        return v

# ---------------- ADMIN ----------------
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# ---------------- STUDENT ----------------
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    country: str
    tel: str = Field(..., validation_alias="phone")
    teacher_id: str = Field(..., validation_alias="teacherId")
    dialect_id: str = Field(..., validation_alias="dialectId")
    package_id: str = Field(..., validation_alias="packageId")
    rating: str = Field(..., validation_alias="rating")
    group_whatsapp: str = Field(..., validation_alias="linkGroup")

    @field_validator("tel")
    def validate_phone(cls, v):
        return validate_phone_value(cls, v)

class StudentUpdata(BaseModel):
    name: str
    email: EmailStr
    country: str
    tel: str = Field(..., validation_alias="phone")
    teacher_id: str = Field(..., validation_alias="teacherId")
    dialect_id: str = Field(..., validation_alias="dialectId")
    package_id: str = Field(..., validation_alias="packageId")
    rating: str = Field(..., validation_alias="rating")
    group_whatsapp: str = Field(..., validation_alias="linkGroup")

    @field_validator("tel")
    def validate_phone(cls, v):
        return validate_phone_value(cls, v)


# ---------------- TEACHER ----------------
class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    country: str
    phone: str
    dialect: list[uuid.UUID]
    rating: str

    @field_validator("phone")
    def validate_phone(cls, v):
        return validate_phone_value(cls, v)

class TeacherUpdate(BaseModel):
    name: str
    email: EmailStr
    country: str
    tel: str = Field(..., validation_alias="phone")
    rating: str

    @field_validator("tel")
    def validate_phone(cls, v):
        return validate_phone_value(cls, v)


# ---------------- PACKAGE ----------------
class PackageCreate(BaseModel):
    name: str
    lesson: str = Field(validation_alias="lesson")
    mount_paid: str = Field(validation_alias="monthly_payment")
    features: List[str]


# ---------------- DIALECTS ----------------
class DialectCreate(BaseModel):
    name: str


class FilterParams(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)
    search: Optional[str] = Field(
        default=None, description="Search term for filtering by name or email"
    )
    country: Optional[str] = Field(default=None, description="Filter by country")
    tel: Optional[str] = Field(
        default=None,
        validation_alias="telephone",
        description="Filter by telephone number",
    )
    

    @field_validator("tel")
    def validate_phone(cls, v):
        if v is not None:
            return validate_phone_value(cls, v)
        return v
class FilterTeacherParams(FilterParams):
    
    dialect : Optional[list[str]] =Field(default=None, description="Filter by dialect")
# class FilterParams(BaseModel):
#     pass


class TeacherDialectModel(BaseModel):
    dialect_id:list[uuid.UUID]
    teacher_id:uuid.UUID
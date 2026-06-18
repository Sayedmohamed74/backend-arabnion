from datetime import datetime
import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    status: int
    message: str
    data: T | None = None
    error: bool = False


class ResponseTokenModel(BaseModel):
    access_token: str
    refresh_token: str


class ResponseUserModel(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    country: str | None = None
    telephone: str | None = Field(..., validation_alias="tel")

    created_at: datetime = Field(..., validation_alias="create_at")


class ResponseStudentModel(ResponseUserModel):
    package_name: str
    dialect_name: str

class ResponseDialectModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str



class ResponseTeacherModel(ResponseUserModel):
    model_config = ConfigDict(from_attributes=True)
    rating:str | None

    dialects: list[ResponseDialectModel] | None


class ResponseModelList(BaseModel, Generic[T]):
    status: int
    message: str
    data: list[T] | None = None
    pagination: dict[str, int] | None = None
    error: bool = False


class ResponseTeacherDialectModel(BaseModel):
    id:str
    name:str
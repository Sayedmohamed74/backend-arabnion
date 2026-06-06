from datetime import datetime

from pydantic import BaseModel, Field
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
    id: int
    name: str
    email: str
    country: str | None = None
    telephone: str | None = Field(..., validation_alias="tel")

    created_at: datetime = Field(..., validation_alias="create_at")



class ResponseModelList(BaseModel, Generic[T]):
    status: int
    message: str
    data: list[T] | None = None
    pagination: dict[str, int] | None = None
    error: bool  = False



from typing import TypedDict, Optional 
from enum import Enum
import datetime


class AdminType(TypedDict):
    id: Optional[int]
    name: str
    email: str
    password: str


class StudentType(TypedDict):
    id: Optional[int]
    name: str
    email: str
    password: str
    country: str
    tel: str


class TeacherType(TypedDict):
    id: Optional[int]
    name: str
    email: str
    password: str
    country: str
    tel: str


class PackageType(TypedDict):
    id: Optional[int]
    name: str
    lesson: str
    mount_paid: str
    features: list[str]
    
    
    

class EncodeTokenType(TypedDict):
    id: int
    email: str
    name: str
    role: str
    exp: int

class InvalidOrExpire(str, Enum):
    EXPIRE = "expire"
    INVALID = 'invalid'
    
    
    
    
class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = 'teacher'
    STUDENT = 'student'
from fastapi import HTTPException
from src.utils.errors import raise_error, ErrorKey
def is_admin(user):
    if "role" in user and user["role"] != "admin":
        raise_error(ErrorKey.UNAUTHORIZED, "Only admin can create teacher accounts")
    return True


def is_teacher(user):
    if "role" in user and user["role"] != "teacher":
        raise_error(ErrorKey.UNAUTHORIZED, "Only teachers can access it")
    return True


def is_student(user):
    if "role" in user and user["role"] != "student":
        raise_error(ErrorKey.UNAUTHORIZED, "Only students can access it")
    return True


def is_invalid_or_expired_token(user):
    if "expired" in user:
        raise HTTPException(status_code=401, detail="Token expired")
    if "invalid" in user:
        raise HTTPException(status_code=401, detail="Invalid token")
from enum import Enum
from fastapi import status, HTTPException


# =========================
# 1. Error Keys (Enum)
# =========================
class ErrorKey(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    BAD_REQUEST = "BAD_REQUEST"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# =========================
# 2. Error Mapping
# =========================
ERROR_MAP = {
    ErrorKey.NOT_FOUND: {
        "status_code": status.HTTP_404_NOT_FOUND,
        "detail": "Resource not found",
    },
    ErrorKey.UNAUTHORIZED: {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Unauthorized access",
    },
    ErrorKey.FORBIDDEN: {
        "status_code": status.HTTP_403_FORBIDDEN,
        "detail": "You don't have permission",
    },
    ErrorKey.BAD_REQUEST: {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "detail": "Bad request data",
    },
    ErrorKey.CONFLICT: {
        "status_code": status.HTTP_409_CONFLICT,
        "detail": "Conflict occurred",
    },
    ErrorKey.INTERNAL_ERROR: {
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": "Internal server error",
    },
}


# =========================
# 3. Raise Helper Function
# =========================
def raise_error(key: ErrorKey, custom_detail: str | None = None):
    error = ERROR_MAP.get(key)

    if not error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unknown error key",
        )

    raise HTTPException(
        status_code=error["status_code"],
        detail=custom_detail or error["detail"],
    )

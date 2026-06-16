import jwt
import os
from datetime import datetime, timedelta, timezone
from src.utils.wrap_response import success_response
from fastapi import security
from typing import Annotated

from fastapi import Depends

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="/auth/", scheme_name="UserAuth")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=15)})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(days=7)})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"expired": True, "invalid": False}
    except jwt.InvalidTokenError:
        return {"invalid": True, "expired": False}

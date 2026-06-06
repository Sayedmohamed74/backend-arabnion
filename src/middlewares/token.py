from fastapi import Request
from fastapi.responses import JSONResponse
from src.utils.wrap_response import success_response
from src.lib.jwt import decode_token


async def auth_token(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token is None:
        return JSONResponse(
            status_code=401, content=success_response(None, "Unauthorized", 401)
        )
    token = token.split(" ")[1] if " " in token else token
    payload = decode_token(token)
    if payload is None:
        return JSONResponse(
            status_code=401, content=success_response(None, "Unauthorized", 401)
        )
    request.state.user = payload
    response = await call_next(request)
    return response

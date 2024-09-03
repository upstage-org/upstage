from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security, Depends, HTTPException, status
import jwt

from authentication.services.auth import AuthenticationService
from config.env import ALGORITHM, SECRET_KEY
from core.exceptions import throw_custom_exception


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return throw_custom_exception(
            status.HTTP_401_UNAUTHORIZED, {"error": "Token has expired"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, {"error": "Invalid token"})


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    authentication_service: AuthenticationService = Depends(),
):
    token = credentials.credentials
    payload = decode_jwt(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = authentication_service.user_service.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

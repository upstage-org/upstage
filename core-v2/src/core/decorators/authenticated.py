from functools import wraps
from fastapi import Request
import jwt
from graphql import GraphQLError
from config.env import ALGORITHM, SECRET_KEY


def authenticated():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            info = args[1]
            request: Request = info.context["request"]
            authorization: str = request.headers.get("Authorization")
            if not authorization:
                raise GraphQLError("Authorization header missing")

            token = authorization.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.current_user = payload

            except jwt.ExpiredSignatureError:
                raise GraphQLError("Token has expired")
            except jwt.InvalidTokenError:
                raise GraphQLError("Invalid token")

            return await func(*args, **kwargs)

        return wrapper

    return decorator

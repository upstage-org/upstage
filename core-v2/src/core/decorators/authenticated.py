from functools import wraps
from fastapi import Request
import jwt
from graphql import GraphQLError
from config.env import ALGORITHM, SECRET_KEY
from users.services.user import UserService


def authenticated(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

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
                current_user = UserService().find_by_id(payload.get("user_id"))
                if not current_user:
                    raise GraphQLError("Invalid token")

                if allowed_roles and current_user.role not in allowed_roles:
                    raise GraphQLError("Permission denied")

                request.state.current_user = current_user.to_dict()

            except jwt.ExpiredSignatureError:
                raise GraphQLError("Signature has expired")
            except jwt.InvalidTokenError:
                raise GraphQLError("Invalid token")

            return func(*args, **kwargs)

        return wrapper

    return decorator

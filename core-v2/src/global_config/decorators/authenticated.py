import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(project_dir)


from functools import wraps
from fastapi import Request
import jwt
from graphql import GraphQLError
from global_config import ALGORITHM, SECRET_KEY
from users.services.user import UserService


def authenticated(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = args[1]
            request: Request = info.context["request"]
            authorization: str = request.headers.get("Authorization")
            if not authorization:
                raise GraphQLError("Authenticated Failed")

            token = authorization.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                current_user = UserService().find_by_id(payload.get("user_id"))
                if not current_user:
                    raise GraphQLError("Authenticated Failed")

                if allowed_roles and current_user.role not in allowed_roles:
                    raise GraphQLError("Permission denied")

                request.state.current_user = current_user.to_dict()

            except jwt.ExpiredSignatureError:
                raise GraphQLError("Signature has expired")
            except jwt.InvalidTokenError:
                raise GraphQLError("Authenticated Failed")

            return func(*args, **kwargs)

        return wrapper

    return decorator

from datetime import datetime, timedelta
from graphql import GraphQLError
import jwt
from fastapi import Request
from email.utils import parseaddr
from authentication.http.validation import LoginInput
from config.database import ScopedSession
from users.entities.user import ADMIN, GUEST, PLAYER, SUPER_ADMIN, UserEntity
from users.services.user import UserService
from core.helpers.fernet_crypto import decrypt
from config.env import (
    ENV_TYPE,
    JWT_ACCESS_TOKEN_MINUTES,
    JWT_HEADER_NAME,
    JWT_REFRESH_TOKEN_DAYS,
    SECRET_KEY,
    ALGORITHM,
)
from authentication.entities.user_session import UserSessionEntity


class AuthenticationService:
    def __init__(self):
        self.user_service = UserService()

    async def login(self, dto: LoginInput, request: Request):
        user: UserEntity = None
        username, password = dto.username, dto.password

        email = self.validate_login_payload(username, password)
        user = self.user_service.find_one(username, email)
        if not user:
            return GraphQLError("Incorrect username or password")

        self.validate_password(password, user)
        access_token = self.create_token(
            {"user_id": user.id}, timedelta(minutes=int(JWT_ACCESS_TOKEN_MINUTES))
        )
        refresh_token = self.create_token(
            {"user_id": user.id, "type": "refresh"},
            timedelta(
                days=int(JWT_REFRESH_TOKEN_DAYS) if user.role == SUPER_ADMIN else 1
            ),
        )

        user_session = UserSessionEntity(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            app_version=request.headers.get("X-Upstage-App-Version"),
            app_os_type=request.headers.get("X-Upstage-Os-Type"),
            app_os_version=request.headers.get("X-Upstage-Os-Version"),
            app_device=request.headers.get("X-Upstage-Device-Model"),
        )

        user.last_login = datetime.utcnow()

        with ScopedSession() as local_db_session:
            local_db_session.add(user_session)
            local_db_session.commit()
            local_db_session.flush()
        self.user_service.update(user)

        title_prefix = "" if ENV_TYPE == "Production" else "DEV "
        default_title = title_prefix + "Upstage"
        title = default_title

        if user.role == SUPER_ADMIN:
            title = title_prefix + "Super Admin"
            group = {"id": 0, "name": "test"}
            groups = [group]

        elif user.role in (PLAYER, GUEST, ADMIN) and not (group):
            group = {"id": 0, "name": "test"}
            groups = [group]

        return dict(
            {
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "role": user.role,
                "first_name": user.first_name,
                "groups": groups,
                "username": user.username,
                "title": title,
            }
        )

    def validate_login_payload(self, username: str, password: str):
        if not username or len(username) == 0 or len(username) > 100:
            raise GraphQLError("Missing/invalid username or email")

        if not password or len(password) == 0 or len(password) > 256:
            raise GraphQLError("Missing/invalid password parameter")

        username = username.strip()
        if "@" in username:
            email = parseaddr(username)[1]
            if not email or len(email) <= 0 or len(email) > 100:
                raise GraphQLError("Invalid username or email")
            return email

    def validate_password(self, enter_password: str, user: UserEntity):
        try:
            if decrypt(user.password) != enter_password:
                raise GraphQLError("Incorrect username or password")
        except:
            raise GraphQLError(
                "Signature did not match digest. Please contact admin to make sure that cipher key is correctly set up."
            )
        if not user.active:
            raise GraphQLError(
                "Your account has been successfully created but not approved yet.<br/>Please wait for approval or contact UpStage Admin for support!"
            )

    def create_token(
        self, data: dict, exp=timedelta(minutes=int(JWT_ACCESS_TOKEN_MINUTES))
    ):
        to_encode = data.copy()
        expire = datetime.now() + exp
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def logout(self, request: Request):
        bearer_token = request.headers.get("Authorization", "").split(" ")
        if len(bearer_token) != 2:
            raise GraphQLError("Invalid access token")

        access_token = bearer_token[1]
        with ScopedSession() as local_db_session:
            user_session = (
                local_db_session.query(UserSessionEntity)
                .filter(UserSessionEntity.access_token == access_token)
                .first()
            )
            if not user_session:
                raise GraphQLError("Invalid access token")
            local_db_session.delete(user_session)

        return "Logged out"

    async def refresh_token(self, user: UserEntity, request: Request):
        refresh_token = request.headers.get(JWT_HEADER_NAME)
        if not refresh_token:
            raise GraphQLError("Invalid refresh token")

        access_token = self.create_token(
            {"user_id": user.id}, timedelta(minutes=int(JWT_ACCESS_TOKEN_MINUTES))
        )

        with ScopedSession() as local_db_session:
            local_db_session.query(UserSessionEntity).filter(
                UserSessionEntity.refresh_token == refresh_token
            ).delete()

            user_session = UserSessionEntity(
                user_id=user.id,
                access_token=access_token,
                refresh_token=refresh_token,
                app_version=request.headers.get("X-Upstage-App-Version"),
                app_os_type=request.headers.get("X-Upstage-Os-Type"),
                app_os_version=request.headers.get("X-Upstage-Os-Version"),
                app_device=request.headers.get("X-Upstage-Device-Model"),
            )
            local_db_session.add(user_session)
            local_db_session.flush()

        user.last_login = datetime.now()
        self.user_service.update(user)

        return {"access_token": access_token}

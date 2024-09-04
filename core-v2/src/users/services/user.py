from operator import or_

from fastapi import Request
from graphql import GraphQLError
import requests
from config.database import DBSession, ScopedSession
from config.env import CLOUDFLARE_CAPTCHA_SECRETKEY, CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT
from core.helpers.fernet_crypto import encrypt
from users.entities.user import PLAYER, UserEntity
from users.http.dtos.signup import SignupDTO


class UserService:
    def __init__(self):
        pass

    def find_one(self, username: str, email: str):
        return (
            DBSession.query(UserEntity)
            .filter(or_(UserEntity.username == username, UserEntity.email == email))
            .first()
        )

    def find_by_id(self, user_id: int):
        return (
            DBSession.query(UserEntity)
            .filter(UserEntity.id == user_id, UserEntity.active.is_(True))
            .first()
        )

    def create(self, data: SignupDTO, request: Request):
        self.verify_captcha(data, request)

        existing_user = self.find_one(data["username"], data.get("email", ""))
        if existing_user:
            raise GraphQLError("User already exists")

        user = UserEntity()

        with ScopedSession() as local_db_session:
            user.password = encrypt(data["password"])
            user.role = PLAYER if not user.role else user.role
            user.active = True
            user.email = data.get("email", "")
            user.first_name = data.get("firstName", "")
            user.last_name = data.get("lastName", "")
            user.username = data.get("username", "")
            user.intro = data.get("intro", "")
            local_db_session.add(user)
            local_db_session.commit()
            local_db_session.flush()

        user = (
            DBSession.query(UserEntity)
            .filter(UserEntity.username == data["username"])
            .first()
        )

        # TODO: Send email

        return {"user": user.to_dict()}

    def verify_captcha(self, data: SignupDTO, request: Request):
        ip = request.headers.get("X-Forwarded-For", request.client.host)
        formData = {
            "secret": CLOUDFLARE_CAPTCHA_SECRETKEY,
            "response": data["token"],
            "remoteip": ip,
        }

        result = requests.post(CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT, data=formData)
        outcome = result.json()

        if not outcome["success"]:
            raise GraphQLError(
                "We think you are not a human! " + ", ".join(outcome["error-codes"])
            )
        else:
            del data["token"]

    def update(self, user: UserEntity):
        return DBSession.merge(user)

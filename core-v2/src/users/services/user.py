from operator import or_

from fastapi import Request
from graphql import GraphQLError
import requests
from global_config import (
    CLOUDFLARE_CAPTCHA_SECRETKEY,
    CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT,
    SUPPORT_EMAILS,
    UPSTAGE_FRONTEND_URL,
    DBSession,
    ScopedSession,
)
from mails.helpers.mail import send
from mails.templates.templates import admin_registration_notification, user_registration
from users.db_models.user import PLAYER, UserModel
from users.http.validation import CreateUserInput


class UserService:
    def __init__(self):
        pass

    def find_one(self, username: str, email: str):
        return (
            DBSession.query(UserModel)
            .filter(or_(UserModel.username == username, UserModel.email == email))
            .first()
        )

    def find_by_id(self, user_id: int):
        return (
            DBSession.query(UserModel)
            .filter(UserModel.id == user_id, UserModel.active.is_(True))
            .first()
        )

    async def create(self, data: CreateUserInput, request: Request):
        self.verify_captcha(data, request)

        existing_user = self.find_one(data["username"], data.get("email", ""))
        if existing_user:
            raise GraphQLError("User already exists")

        user = UserModel()

        with ScopedSession() as local_db_session:
            from global_config import encrypt

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
            DBSession.query(UserModel)
            .filter(UserModel.username == data["username"])
            .first()
        )

        await send([user.email], f"Welcome to UpStage!", user_registration(user))
        admin_emails = SUPPORT_EMAILS
        approval_url = f"{UPSTAGE_FRONTEND_URL}/admin/player?sortByCreated=true"
        await send(
            admin_emails,
            f"Approval required for {user.username}'s registration",
            admin_registration_notification(user, approval_url),
        )

        return {"user": user.to_dict()}

    def verify_captcha(self, data: CreateUserInput, request: Request):
        ip = request.headers.get("X-Forwarded-For", request.client.host)
        formData = {
            "secret": CLOUDFLARE_CAPTCHA_SECRETKEY,
            "response": data["token"],
            "remoteip": ip,
        }

        if not CLOUDFLARE_CAPTCHA_SECRETKEY:
            return

        result = requests.post(CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT, data=formData)
        outcome = result.json()

        if not outcome["success"]:
            raise GraphQLError(
                "We think you are not a human! " + ", ".join(outcome["error-codes"])
            )
        else:
            del data["token"]

    def update(self, user: UserModel):
        DBSession.query(UserModel).filter(UserModel.id == user.id).update(
            {**user.to_dict()}
        )
        DBSession.commit()
        DBSession.flush()

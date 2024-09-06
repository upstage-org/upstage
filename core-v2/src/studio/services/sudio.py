from datetime import datetime
from typing import List

from sqlalchemy import asc, desc, or_
from config.database import DBSession, ScopedSession
from core.helpers.fernet_crypto import encrypt
from core.helpers.object import convert_keys_to_camel_case
from studio.http.validation import BatchUserInput
from users.entities.user import GUEST, UserEntity
from graphql import GraphQLError


class StudioService:
    def __init__(self):
        pass

    def admin_players(self, params):
        totalCount = DBSession.query(UserEntity).count()
        query = DBSession.query(UserEntity)

        if "usernameLike" in params:
            query = query.filter(
                UserEntity.username.ilike(f"%{params['usernameLike']}%")
            )

        if "createdBetween" in params:
            start_date = datetime.strptime(params["createdBetween"][0], "%Y-%m-%d")
            end_date = datetime.strptime(params["createdBetween"][1], "%Y-%m-%d")
            query = query.filter(UserEntity.created_on.between(start_date, end_date))

        if "sort" in params:
            for sort_param in params["sort"]:
                if sort_param == "USERNAME_ASC":
                    query = query.order_by(asc(UserEntity.username))
                elif sort_param == "USERNAME_DESC":
                    query = query.order_by(desc(UserEntity.username))
                elif sort_param == "CREATED_ON_ASC":
                    query = query.order_by(asc(UserEntity.created_on))
                elif sort_param == "CREATED_ON_DESC":
                    query = query.order_by(desc(UserEntity.created_on))

        if "first" in params:
            limit = params["first"] or 10
            page = 0 if "page" not in params else (params["page"] - 1)
            offset = page * limit
            query = query.limit(limit).offset(offset)

        results = query.all()

        return convert_keys_to_camel_case(
            {"totalCount": totalCount, "edges": [user.to_dict() for user in results]}
        )

    def create_users(self, users: List[BatchUserInput]):
        with ScopedSession() as session:
            self.validate_user_information(users, session)

            for user in users:
                user = UserEntity(
                    username=user["username"],
                    email=user["email"],
                    active=True,
                    role=GUEST,
                    password=encrypt(user["password"]),
                )
                session.add(user)
            session.commit()

        users = (
            DBSession.query(UserEntity)
            .filter(UserEntity.email.in_([user["email"] for user in users]))
            .all()
        )
        return convert_keys_to_camel_case({"users": [user.to_dict() for user in users]})

    def validate_user_information(self, users: List[BatchUserInput], session):
        for user in users:
            BatchUserInput(**user)

        duplicated = []
        for i in range(len(users) - 1):
            for j in range(i + 1, len(users)):
                if (
                    users[i]["username"] == users[j]["username"]
                    or users[i]["email"] == users[j]["email"]
                ):
                    duplicated.append(users[i]["username"])

        if duplicated:
            raise GraphQLError(f"Duplicated user information {''.join(duplicated)}")

        existing_users = (
            session.query(UserEntity)
            .filter(
                or_(
                    UserEntity.username.in_([user["username"] for user in users]),
                    UserEntity.email.in_([user["email"] for user in users]),
                )
            )
            .all()
        )

        if existing_users:
            raise GraphQLError(
                f"Users with emails {', '.join([user.email for user in existing_users])} already exist"
            )

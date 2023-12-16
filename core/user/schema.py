# -*- coding: iso8859-15 -*-
from datetime import datetime
from core.auth.models import UserSession
from core.mail.mail_utils import send
from core.mail.templates import (
    admin_registration_notification,
    user_approved,
    user_registration,
)
from core.asset.models import (
    Stage as StageModel,
    StageAttribute as StageAttributeModel,
    Asset as AssetModel,
)
from core.performance_config.models import ParentStage as ParentStageModel, Performance
import sys, os
import json
import uuid
import requests

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

import graphene
from graphene import relay
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from core.project_globals import (
    DBSession,
    Base,
    metadata,
    engine,
    ScopedSession,
    app,
    api,
    ScopedSession,
)
from config import (
    URL_PREFIX,
    SUPPORT_EMAILS,
    CLOUDFLARE_CAPTCHA_SECRETKEY,
    CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT,
)
from core.auth.auth_api import jwt_required
from core.user.models import (
    ADMIN,
    GUEST,
    PLAYER,
    SUPER_ADMIN,
    OneTimeTOTP,
    User as UserModel,
)
from flask_graphql import GraphQLView
from core.auth.fernet_crypto import encrypt, decrypt
from core.utils import graphql_utils
from core.auth.auth_mutation import (
    AuthMutation,
    PasswordResetMutation,
    RefreshMutation,
    RequestPasswordResetMutation,
    VerifyPasswordResetMutation,
)
from core.user.user_utils import current_user
from flask_jwt_extended import jwt_required
from flask import request
from graphql_relay.node.node import from_global_id


class UserAttribute:
    username = graphene.String(description="Username")
    password = graphene.String(description="Password")
    email = graphene.String(description="Email Address")
    bin_name = graphene.String(description="bin_name")
    role = graphene.Int(description="User Role")
    first_name = graphene.String(description="First Name")
    last_name = graphene.String(description="Last Name")
    display_name = graphene.String(description="Display Name")
    active = graphene.Boolean(description="Active record or not")
    firebase_pushnot_id = graphene.String(description="firebase_pushnot_id")
    upload_limit = graphene.Int(description="Maximum file upload size limit, in bytes")
    intro = graphene.String(description="Introduction")


class User(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = UserModel
        interfaces = (relay.Node,)
        connection_class = graphql_utils.CountableConnection

    def resolve_db_id(self, info):
        return self.id


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to create a user."""

    token = graphene.String(description="Cloudflare captcha token.")


class CreateUser(graphene.Mutation):
    """Mutation to create a user."""

    user = graphene.Field(lambda: User, description="User created by this mutation.")

    class Arguments:
        inbound = CreateUserInput(required=True)

    async def mutate(self, info, inbound):
        data = graphql_utils.input_to_dictionary(inbound)
        # We have GUEST role because Helen wants to create batch users for demo purposes
        # GUEST users don't neccessarily need an email address to keep batch creation simple
        if data["email"] in ("", None):
            if data["role"] != GUEST:
                raise Exception("Email is required!")
            data["email"] = str(uuid.uuid4()) + "@stub.stub"
        if not data["intro"]:
            raise Exception("Introduction is required!")

        if not data["token"]:
            raise Exception("You are not a human!")

        # Validate the token by calling the verify API endpoint.
        ip = request.headers.get("CF-Connecting-IP")
        formData = {
            "secret": CLOUDFLARE_CAPTCHA_SECRETKEY,
            "response": data["token"],
            "remoteip": ip,
        }

        result = requests.post(CLOUDFLARE_CAPTCHA_VERIFY_ENDPOINT, data=formData)
        outcome = result.json()

        if not outcome["success"]:
            raise Exception("You are not a human! " + ", ".join(outcome["error-codes"]))
        else:
            del data["token"]

        user = UserModel(**data)
        user_id = None
        # Add validation for non-empty passwords, etc.
        user.password = encrypt(user.password)
        if not user.role:
            user.role = PLAYER
        with ScopedSession() as local_db_session:
            local_db_session.add(user)
            local_db_session.flush()
            user_id = user.id

        user = DBSession.query(UserModel).filter(UserModel.id == user_id).first()
        await send([user.email], f"Welcome to UpStage!", user_registration(user))
        # No, don't send this to every admin.
        # admin_emails = [admin.email for admin in DBSession.query(UserModel).filter(UserModel.role.in_([SUPER_ADMIN,ADMIN])).all()]
        admin_emails = SUPPORT_EMAILS
        approval_url = f"{request.url_root}backstage/admin/player-management"
        await send(
            admin_emails,
            f"Approval required for {user.username}'s registration",
            admin_registration_notification(user, approval_url),
        )
        return CreateUser(user=user)


class UpdateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to update a user."""

    id = graphene.ID(required=True, description="Global Id of the user.")


class UpdateUser(graphene.Mutation):
    """Update a user."""

    user = graphene.Field(lambda: User, description="User updated by this mutation.")

    class Arguments:
        inbound = UpdateUserInput(required=True)

    @jwt_required()
    async def mutate(self, info, inbound):
        data = graphql_utils.input_to_dictionary(inbound)
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN):
            if not user.id == int(data["id"]):
                raise Exception("Permission denied!")

        if data["email"] in ("", None):
            if data["role"] != GUEST:
                raise Exception("Email is required!")
            data["email"] = str(uuid.uuid4()) + "@stub.stub"

        with ScopedSession() as local_db_session:
            try:
                user = (
                    local_db_session.query(UserModel)
                    .filter(UserModel.id == data["id"])
                    .first()
                )
                if data["password"]:
                    data["password"] = encrypt(data["password"])
                else:
                    del data["password"]
                for key, value in data.items():
                    if key == "active":
                        if value and not user.active and not user.deactivated_on:
                            await send(
                                [user.email],
                                f"Registration approved for user {user.username}",
                                user_approved(user),
                            )
                        if not value and user.active:
                            user.deactivated_on = datetime.now()

                    if hasattr(user, key):
                        setattr(user, key, value)
                local_db_session.flush()
            except Exception as e:
                if "email" in e.args[0]:
                    raise Exception(
                        f"This email address already belongs to another user!"
                    )
                app.logger.error(e)
                raise Exception(
                    f"There was an error updating this user information. Please check the logs and try again later.!"
                )

        user = DBSession.query(UserModel).filter(UserModel.id == data["id"]).first()
        return UpdateUser(user=user)


class OneUserInput(graphene.InputObjectType):
    """This is used to get one user's data, including their global ID.
    This is why the global ID is not required.
    You should be able to pass nothing and get data on your own logged-in user,
    because of the JWT token."""

    id = graphene.ID(required=False, description="Global Id of the user.")
    username = graphene.String(required=False)
    db_id = graphene.Int(required=False)
    email = graphene.String(required=False)


class OneUser(graphene.ObjectType):
    # search = OneUserInput()

    """User lookup. If not an admin, you can only look yourself up,
    and only if you're logged in."""

    class Arguments:
        """Looking up current user requires no arguments."""

        inbound = OneUserInput(required=False)

    @jwt_required()
    def resolve_search(self, info, inbound):
        """Get user from JWT token."""
        code, error, this_user, timezone = current_user()
        if code != 200:
            raise Exception(error)

        """ Compare it with params. If current user is an admin, allow lookup
            of other users.
        """
        if inbound:
            data = graphql_utils.input_to_dictionary(inbound)
            lookup_user = DBSession.query(UserModel).filter_by(data).first()

        access_token = request.headers.get(app.config["JWT_HEADER_NAME"], None)
        # app.logger.info("access token:{0}".format(access_token))

        # If latest user session access token doesn't match, kick them out.
        user_session = (
            DBSession.query(UserSession)
            .filter(UserSession.user_id == user.id)
            .order_by(UserSession.recorded_time.desc())
            .first()
        )

        if not user_session:
            raise Exception("Bad user session")

        if user_session.access_token != access_token:
            TNL.add(access_token)
            # No. user session may be valid, from a newer login on a different device.
            # TNL.add(user_session.refresh_token)
            # TNL.add(user_session.access_token)
            raise Exception("Access token is invalid")

        self.result = {
            "user_id": user.id,
            "role": user.role,
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "timezone": timezone,
            "groups": [],
            "username": user.username,
        }
        # return result
        return graphql_utils.json2obj(self.result)


class ChangePasswordInput(
    graphene.InputObjectType,
    UserAttribute,
):
    """Arguments to update a user."""

    id = graphene.ID(required=True, description="Global Id of the user.")
    oldPassword = graphene.String(required=True)
    newPassword = graphene.String(required=True)


class ChangePassword(graphene.Mutation):
    success = graphene.Boolean(description="Password changed successful or not")

    class Arguments:
        inbound = ChangePasswordInput(required=True)

    @jwt_required()
    def mutate(self, info, inbound):
        data = graphql_utils.input_to_dictionary(inbound)
        with ScopedSession() as local_db_session:
            user = (
                local_db_session.query(UserModel)
                .filter(UserModel.id == data["id"])
                .first()
            )
            if decrypt(user.password) != data["oldPassword"]:
                raise Exception("Old password incorrect")
            else:
                user.password = encrypt(data["newPassword"])
            local_db_session.commit()
        return ChangePassword(success=True)


class DeleteUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to update a user."""

    id = graphene.ID(required=True, description="Global Id of the user.")


class DeleteUser(graphene.Mutation):
    success = graphene.Boolean(description="Password changed successful or not")

    class Arguments:
        inbound = DeleteUserInput(required=True)

    @jwt_required()
    def mutate(self, info, inbound):
        data = graphql_utils.input_to_dictionary(inbound)
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN):
            raise Exception("Permission denied!")
        with ScopedSession() as local_db_session:
            # Delete all existed user's sessions
            local_db_session.query(UserSession).filter(
                UserSession.user_id == data["id"]
            ).delete()
            local_db_session.query(OneTimeTOTP).filter(
                OneTimeTOTP.user_id == data["id"]
            ).delete()
            # Delete all stages created by this user
            local_db_session.query(StageAttributeModel).filter(
                StageAttributeModel.stage.has(StageModel.owner_id == data["id"])
            ).delete(synchronize_session="fetch")
            local_db_session.query(ParentStageModel).filter(
                ParentStageModel.stage.has(StageModel.owner_id == data["id"])
            ).delete(synchronize_session="fetch")
            local_db_session.query(Performance).filter(
                Performance.stage.has(StageModel.owner_id == data["id"])
            ).delete(synchronize_session="fetch")
            local_db_session.query(StageModel).filter(
                StageModel.owner_id == data["id"]
            ).delete()
            # Change the owner of media uploaded by this user to the one who process the delete
            # Because delete the media would cause impact to other stage, this would be a workaround for now
            local_db_session.query(AssetModel).filter(
                AssetModel.owner_id == data["id"]
            ).update({AssetModel.owner_id: user.id})
            # Delete the actual user
            local_db_session.query(UserModel).filter(
                UserModel.id == data["id"]
            ).delete()
            local_db_session.commit()
        return DeleteUser(success=True)


class BatchUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class BatchUserCreation(graphene.Mutation):
    """Mutation to create a user."""

    users = graphene.List(User, description="Users created by this mutation.")

    class Arguments:
        users = graphene.List(BatchUserInput, required=True)
        stageIds = graphene.List(graphene.Int, required=False)

    @jwt_required()
    def mutate(self, info, users, stageIds=[]):
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN):
            raise Exception("Permission denied!")
        ids = []
        with ScopedSession() as local_db_session:
            duplicated = []
            for i in range(len(users) - 1):
                for j in range(i + 1, len(users)):
                    if users[i].username == users[j].username:
                        duplicated.append(users[i].username)
            if duplicated:
                raise Exception("Duplicated username: " + ", ".join(duplicated))

            existed = [
                user.username
                for user in DBSession.query(UserModel)
                .filter(UserModel.username.in_([x.username for x in users]))
                .all()
            ]
            if existed:
                raise Exception("Username already existed: " + ", ".join(existed))
            for item in users:
                user = UserModel(username=item.username, active=True, role=GUEST)
                # Add validation for non-empty passwords, etc.
                user.password = encrypt(item.password)
                local_db_session.add(user)
                local_db_session.flush()
                ids.append(user.id)

            # Now assigns users into stages
            stages = (
                DBSession.query(StageModel).filter(StageModel.id.in_(stageIds)).all()
            )
            for stage in stages:
                player_access = stage.attributes.filter(
                    StageAttributeModel.name == "playerAccess"
                ).first()
                if player_access:
                    accesses = json.loads(player_access.description)
                    for user_id in ids:
                        if user_id not in accesses[0]:
                            accesses[0].append(user_id)  # append user id to player ids
                    player_access.description = json.dumps(accesses)
                    local_db_session.flush()

            local_db_session.commit()
        users = DBSession.query(UserModel).filter(UserModel.id.in_(ids)).all()
        return BatchUserCreation(users=users)


class UserConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ["first", "last", "before", "after"]

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(UserConnectionField, cls).get_query(model, info, sort, **args)
        for field, value in args.items():
            if field == "id":
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
            elif len(field) > 5 and field[-4:] == "like":
                query = query.filter(getattr(model, field[:-5]).ilike(f"%{value}%"))
            elif field not in cls.RELAY_ARGS and hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
        return query


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Mutation(graphene.ObjectType):
    """Some mutations are imported from core.auth/"""

    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    authUser = AuthMutation.Field()
    refreshUser = RefreshMutation.Field()
    changePassword = ChangePassword.Field()
    deleteUser = DeleteUser.Field()
    batchUserCreation = BatchUserCreation.Field()
    requestPasswordReset = RequestPasswordResetMutation.Field()
    verifyPasswordReset = VerifyPasswordResetMutation.Field()
    passwordReset = PasswordResetMutation.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    userList = UserConnectionField(
        User.connection,
        id=graphene.ID(),
        username_like=graphene.String(),
        active=graphene.Boolean(),
    )

    # oneUser = graphql_utils.FilteredConnectionField(User, OneUserInput)
    # oneUser = OneUser.search
    currentUser = graphene.Field(User)

    @jwt_required()
    def resolve_currentUser(self, info):
        code, error, user, timezone = current_user()
        if error:
            raise Exception(error)
        return user


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
user_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f"/{URL_PREFIX}user_graphql/",
    view_func=GraphQLView.as_view(
        "user_graphql", schema=user_schema, graphiql=True, executor=AsyncioExecutor()
    ),
)

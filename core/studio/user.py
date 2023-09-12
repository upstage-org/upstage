from datetime import datetime
import os
import sys
from flask_jwt_extended import jwt_required
import graphene

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, ".."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.auth.models import UserSession
from core.utils.graphql_utils import CountableConnection
from core.project_globals import DBSession
from core.mail.mail_utils import send
from core.mail.templates import user_approved
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from core.project_globals import DBSession, ScopedSession, app, ScopedSession
from core.auth.auth_api import jwt_required
from core.user.models import (
    ADMIN,
    GUEST,
    SUPER_ADMIN,
    User as UserModel,
    OneTimeTOTP,
    role_conv,
)
from core.auth.fernet_crypto import decrypt, encrypt
from core.utils import graphql_utils
from core.user.user_utils import current_user
from flask_jwt_extended import jwt_required
from core.asset.models import (
    Stage as StageModel,
    StageAttribute as StageAttributeModel,
    Asset as AssetModel,
)
from core.performance_config.models import ParentStage as ParentStageModel, Performance


class AdminPlayer(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    permission = graphene.String(description="Player access to this user")
    role_name = graphene.String(description="Name of the role")
    last_login = graphene.DateTime(description="Last login time")

    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnection

    def resolve_role_name(self, info):
        return role_conv(self.role)


class UserConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ["first", "last", "before", "after"]

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(UserConnectionField, cls).get_query(model, info, sort, **args)

        verify_jwt_in_request(True)
        for field, value in args.items():
            if field == "id":
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
            elif field == "created_between":
                if len(value) == 2:
                    query = query.filter(AssetModel.created_on >= value[0]).filter(
                        AssetModel.created_on <= value[1]
                    )
            elif len(field) > 5 and field[-4:] == "like":
                query = query.filter(getattr(model, field[:-5]).ilike(f"%{value}%"))
            elif field not in cls.RELAY_ARGS and hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
        return query


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


class UpdateUserInput(graphene.InputObjectType, UserAttribute):
    """Arguments to update a user."""

    id = graphene.ID(required=True, description="Global Id of the user.")


class UpdateUser(graphene.Mutation):
    """Update a user."""

    user = graphene.Field(
        lambda: AdminPlayer, description="User updated by this mutation."
    )

    class Arguments:
        inbound = UpdateUserInput(required=True)

    @jwt_required()
    async def mutate(self, info, inbound):
        data = graphql_utils.input_to_dictionary(inbound)
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN):
            if not user.id == int(data["id"]):
                raise Exception("Permission denied!")

        if not data["email"] and data["role"] != GUEST:
            raise Exception("Email is required!")

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

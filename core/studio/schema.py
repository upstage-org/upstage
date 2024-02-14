# -*- coding: iso8859-15 -*-
import os
import sys
import graphene

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.asset.models import Stage as StageModel
from core.asset.models import Tag as TagModel
from core.auth.auth_mutation import AuthMutation, RefreshMutation
from core.project_globals import DBSession, app
from config import URL_PREFIX
from flask_graphql import GraphQLView
from flask_jwt_extended.view_decorators import jwt_required
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql.execution.executors.asyncio import AsyncioExecutor
from core.stage.asset import DeleteMedia
from core.stage.schema import UpdateAttributeStatus, UpdateAttributeVisibility
from core.user.models import User as UserModel, ADMIN, SUPER_ADMIN, role_conv
from core.user.user_utils import current_user
from core.studio.media import (
    Asset,
    AssetConnectionField,
    AssetType,
    CalcSizes,
    ConfirmPermission,
    QuickAssignMutation,
    RequestPermission,
    SaveMedia,
    UploadFile,
    Voice,
    resolve_voices,
)
from core.studio.stage import StageConnectionField, Stage
from core.studio.notification import Notification, resolve_notifications
from core.studio.user import (
    BatchUserCreation,
    DeleteUser,
    UpdateUser,
    UserConnectionField,
    AdminPlayer,
)
from core.mail.mail_utils import send


class Tag(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = TagModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)


class User(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    role_name = graphene.String(description="Name of the role")

    class Meta:
        model = UserModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)

    def resolve_role_name(self, info):
        return role_conv(self.role)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    mediaTypes = SQLAlchemyConnectionField(AssetType.connection)
    tags = SQLAlchemyConnectionField(Tag.connection)
    users = UserConnectionField(User.connection, active=graphene.Boolean())
    media = AssetConnectionField(
        Asset.connection,
        id=graphene.ID(),
        name_like=graphene.String(),
        created_between=graphene.List(graphene.Date),
        file_location=graphene.String(),
        media_types=graphene.List(graphene.String),
        owners=graphene.List(graphene.String),
        stages=graphene.List(graphene.Int),
        tags=graphene.List(graphene.String),
    )
    stages = StageConnectionField(
        Stage.connection,
        id=graphene.ID(),
        name_like=graphene.String(),
        created_between=graphene.List(graphene.Date),
        file_location=graphene.String(),
        owners=graphene.List(graphene.String),
    )
    adminPlayers = UserConnectionField(
        AdminPlayer.connection,
        id=graphene.ID(),
        username_like=graphene.String(),
        created_between=graphene.List(graphene.Date),
        role=graphene.Int(),
    )
    whoami = graphene.Field(User, description="Logged in user info")
    notifications = graphene.List(Notification, resolver=resolve_notifications)
    voices = graphene.List(Voice, resolver=resolve_voices)

    @jwt_required()
    def resolve_whoami(self, info):
        code, error, user, timezone = current_user()
        return user


class SendEmail(graphene.Mutation):
    """Mutation to customise foyer."""

    success = graphene.Boolean(description="True if the config was saved.")

    class Arguments:
        subject = graphene.String(
            required=True, description="The subject of the email."
        )
        body = graphene.String(
            required=True, description="The body of the email. HTML is allowed."
        )
        recipients = graphene.String(
            required=True, description="The recipients of the email. Comma separated."
        )
        bcc = graphene.String(
            required=False,
            description="The bcc recipients of the email. Comma separated.",
        )

    @jwt_required()
    async def mutate(self, info, subject, body, recipients, bcc):
        code, error, user, timezone = current_user()
        if not user.role in (ADMIN, SUPER_ADMIN) and not user.can_send_email:
            raise Exception("Only Admin can send notification emails!")

        await send(recipients.split(","), subject, body, bcc.split(","))
        return SendEmail(success=True)


class Mutation(graphene.ObjectType):
    calcSizes = CalcSizes.Field()
    deleteMedia = DeleteMedia.Field()
    uploadFile = UploadFile.Field()
    saveMedia = SaveMedia.Field()
    authUser = AuthMutation.Field()
    refreshUser = RefreshMutation.Field()
    confirmPermission = ConfirmPermission.Field()
    requestPermission = RequestPermission.Field()
    quickAssignMutation = QuickAssignMutation.Field()
    updateStatus = UpdateAttributeStatus.Field()
    updateVisibility = UpdateAttributeVisibility.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()
    batchUserCreation = BatchUserCreation.Field()
    sendEmail = SendEmail.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
studio_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f"/{URL_PREFIX}studio_graphql/",
    view_func=GraphQLView.as_view(
        "studio_graphql",
        schema=studio_schema,
        graphiql=True,
        executor=AsyncioExecutor(),
    ),
)

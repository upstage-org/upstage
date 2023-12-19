# -*- coding: iso8859-15 -*-
import os
import sys
from flask_jwt_extended.view_decorators import jwt_required

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from auth.auth_mutation import RefreshMutation
from config.project_globals import DBSession, app
from config.settings import URL_PREFIX
from flask_graphql import GraphQLView
from graphene import relay
from asset.models import Stage as StageModel, Tag as TagModel
from stage.asset import DeleteMedia
from studio.notification import Notification, resolve_notifications
from user.models import ROLES, User as UserModel, role_conv
from studio.media import (Asset, AssetConnectionField,
                          AssetType, CalcSizes, ConfirmPermission, RequestPermission, SaveMedia, UploadFile, Voice, resolve_voices)
from user.user_utils import current_user

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


class Stage(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    permission = graphene.String(description="Player access to this stage")

    class Meta:
        model = StageModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)


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
    stages = SQLAlchemyConnectionField(Stage.connection)
    tags = SQLAlchemyConnectionField(Tag.connection)
    users = SQLAlchemyConnectionField(User.connection)
    media = AssetConnectionField(
        Asset.connection, id=graphene.ID(), name_like=graphene.String(), created_between=graphene.List(graphene.Date), file_location=graphene.String(), media_types=graphene.List(graphene.String), owners=graphene.List(graphene.String), stages=graphene.List(graphene.Int), tags=graphene.List(graphene.String))
    whoami = graphene.Field(User, description="Logged in user info")
    notifications = graphene.List(Notification, resolver=resolve_notifications)
    voices = graphene.List(Voice, resolver=resolve_voices)

    @jwt_required()
    def resolve_whoami(self, info):
        code, error, user, timezone = current_user()
        return user


class Mutation(graphene.ObjectType):
    calcSizes = CalcSizes.Field()
    deleteMedia = DeleteMedia.Field()
    uploadFile = UploadFile.Field()
    saveMedia = SaveMedia.Field()
    refreshUser = RefreshMutation.Field()
    confirmPermission = ConfirmPermission.Field()
    requestPermission = RequestPermission.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
studio_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{URL_PREFIX}/studio_graphql/', view_func=GraphQLView.as_view(
        "studio_graphql", schema=studio_schema,
        graphiql=True
    )
)

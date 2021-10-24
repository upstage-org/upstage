# -*- coding: iso8859-15 -*-
import os
import sys

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from config.project_globals import app
from config.settings import VERSION
from flask_graphql import GraphQLView
from graphene import relay
from asset.models import Stage as StageModel
from user.models import User as UserModel
from studio.media import (Asset, AssetConnectionField, AssetType, CalcSizes)

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


class User(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = UserModel
        model.db_id = model.id
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    mediaTypes = SQLAlchemyConnectionField(AssetType.connection)
    stages = SQLAlchemyConnectionField(Stage.connection)
    users = SQLAlchemyConnectionField(User.connection)
    media = AssetConnectionField(
        Asset.connection, id=graphene.ID(), name_like=graphene.String(), created_between=graphene.List(graphene.Date), file_location=graphene.String(), media_types=graphene.List(graphene.String), owners=graphene.List(graphene.String), stages=graphene.List(graphene.Int))


class Mutation(graphene.ObjectType):
    calcSizes = CalcSizes.Field()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
studio_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/studio_graphql/', view_func=GraphQLView.as_view(
        "studio_graphql", schema=studio_schema,
        graphiql=True
    )
)

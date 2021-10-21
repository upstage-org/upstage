# -*- coding: iso8859-15 -*-
import os
import sys

import graphene
from config.project_globals import app
from config.settings import VERSION
from flask_graphql import GraphQLView
from graphene import relay

from studio.media import (Asset, AssetConnectionField, AssetType, AssignStages,
                          DeleteMedia, UpdateMedia, UploadMedia)
from studio.stage import Stage, StageConnectionField

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


class Mutation(graphene.ObjectType):
    uploadMedia = UploadMedia.Field()
    updateMedia = UpdateMedia.Field()
    deleteMedia = DeleteMedia.Field()
    assignStages = AssignStages.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    stages = StageConnectionField(
        Stage.connection, id=graphene.ID(), name_like=graphene.String(), file_location=graphene.String())
    media = AssetConnectionField(
        Asset.connection, id=graphene.ID(), name_like=graphene.String(), asset_type=graphene.String(), file_location=graphene.String())
    mediaTypes = StageConnectionField(
        AssetType.connection, id=graphene.ID(), name_like=graphene.String())


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
studio_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/studio_graphql/', view_func=GraphQLView.as_view(
        "studio_graphql", schema=studio_schema,
        graphiql=True
    )
)

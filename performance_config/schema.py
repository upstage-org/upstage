# -*- coding: iso8859-15 -*-
from datetime import datetime
import os
import sys

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir,'..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from config.project_globals import DBSession
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from performance_config.models import (ParentStage as ParentStageModel, ParentAsset as ParentAssetModel,
    PerformanceConfig as PerformanceConfigModel, Scene as SceneModel,
    PerformanceMQTTConfig as PerformanceMQTTConfigModel)

class ParentStage(SQLAlchemyObjectType):
    class Meta:
        model = ParentStageModel
        interfaces = (relay.Node, )

class ParentAsset(SQLAlchemyObjectType):
    class Meta:
        model = ParentAssetModel
        interfaces = (relay.Node, )

class PerformanceConfig(SQLAlchemyObjectType):
    class Meta:
        model = PerformanceConfigModel
        interfaces = (relay.Node, )

class Scene(SQLAlchemyObjectType):
    class Meta:
        model = SceneModel
        interfaces = (relay.Node, )

class PerformanceMQTTConfig(SQLAlchemyObjectType):
    class Meta:
        model = PerformanceMQTTConfigModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    parent_stage = SQLAlchemyConnectionField(ParentStage.connection)
    parent_asset = SQLAlchemyConnectionField(ParentStage.connection)
    performance_config = SQLAlchemyConnectionField(PerformanceConfig.connection)
    scene = SQLAlchemyConnectionField(Scene.connection)
    performance_communication = SQLAlchemyConnectionField(PerformanceMQTTConfig.connection)

performance_schema = graphene.Schema(query=Query)
schema.execute(context_value={'session': session})

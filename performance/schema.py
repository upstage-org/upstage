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
from performance.models import (ParentStage as ParentStageModel, ParentAsset as ParentAssetModel,
    Performance as PerformanceModel, Scene as SceneModel,
    LivePerformanceCommunication as LivePerformanceCommunicationModel)

class ParentStage(SQLAlchemyObjectType):
    class Meta:
        model = ParentStageModel
        interfaces = (relay.Node, )

class ParentAsset(SQLAlchemyObjectType):
    class Meta:
        model = ParentAssetModel
        interfaces = (relay.Node, )

class Performance(SQLAlchemyObjectType):
    class Meta:
        model = PerformanceModel
        interfaces = (relay.Node, )

class Scene(SQLAlchemyObjectType):
    class Meta:
        model = SceneModel
        interfaces = (relay.Node, )

class LivePerformanceCommunication(SQLAlchemyObjectType):
    class Meta:
        model = LivePerformanceCommunicationModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    parent_stage = SQLAlchemyConnectionField(ParentStage.connection)
    parent_asset = SQLAlchemyConnectionField(ParentStage.connection)
    performance = SQLAlchemyConnectionField(Performance.connection)
    scene = SQLAlchemyConnectionField(Scene.connection)
    live_performance_communication = SQLAlchemyConnectionField(LivePerformanceCommunication.connection)

performance_schema = graphene.Schema(query=Query)
schema.execute(context_value={'session': session})

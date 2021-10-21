# -*- coding: iso8859-15 -*-
import graphene
from asset.models import Stage as StageModel
from asset.models import StageAttribute as StageAttributeModel
from config.project_globals import (Base, DBSession, api, app, engine,
                                    get_scoped_session, metadata)
from event_archive.models import Event as EventModel
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql_relay.node.node import from_global_id
from performance_config.models import Performance as PerformanceModel
from performance_config.models import Scene as SceneModel
from utils import graphql_utils


class StageAttribute:
    name = graphene.String(description="Stage Name")
    description = graphene.String(description="Stage Description")
    file_location = graphene.String(description="Unique File Location")
    status = graphene.String(description="Live/Upcoming/Rehearsal")
    cover = graphene.String(description="Cover image url")
    media = graphene.String(description="Media attached to stage")
    config = graphene.String(description="Stage configurations")
    playerAccess = graphene.String(
        description="Users who can access and edit this stage")


class StageAttributes(SQLAlchemyObjectType):
    class Meta:
        model = StageAttributeModel


class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel


class Media(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    type = graphene.String()
    src = graphene.String()
    description = graphene.String()


class Stage(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    events = graphene.List(
        Event, description="Archived events of this performance", performance_id=graphene.Int(), cursor=graphene.Int())
    chats = graphene.List(
        Event, description="All chat sent by players and audiences")
    permission = graphene.String(description="Player access to this stage")
    media = graphene.List(Media, description="Media assigned to this stage")

    class Meta:
        model = StageModel
        model.db_id = model.id
        interfaces = (relay.Node,)
        connection_class = graphql_utils.CountableConnection

    def resolve_media(self, info):
        return [{
            'id': x.child_asset.id,
            'name': x.child_asset.name,
            'type': x.child_asset.asset_type.name,
            'src': x.child_asset.file_location,
            'description': x.child_asset.description
        } for x in self.assets.all()]

    def resolve_scenes(self, info, performance_id=None):
        query = DBSession.query(SceneModel)\
            .filter(SceneModel.stage_id == self.db_id)\
            .order_by(SceneModel.scene_order.asc())
        if not performance_id:  # Only fetch disabled scene in performance replay
            query = query.filter(SceneModel.active == True)
        scenes = query.all()
        return scenes

    def resolve_active_recording(self, info):
        recording = DBSession.query(PerformanceModel)\
            .filter(PerformanceModel.stage_id == self.db_id)\
            .filter(PerformanceModel.recording == True)\
            .filter(PerformanceModel.saved_on == None)\
            .first()
        return recording


class StageConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ['first', 'last', 'before', 'after']

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(StageConnectionField, cls).get_query(
            model, info, sort, **args)
        for field, value in args.items():
            if field == 'id':
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
            elif field == 'asset_type':
                query = query.filter(getattr(model, field).has(name=value))
            elif len(field) > 5 and field[-4:] == 'like':
                query = query.filter(
                    getattr(model, field[:-5]).ilike(f"%{value}%"))
            elif field not in cls.RELAY_ARGS and hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
        return query

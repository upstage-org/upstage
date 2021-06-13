# -*- coding: iso8859-15 -*-
from user.user_utils import current_user
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required, verify_jwt_in_request
import performance_config.models
from performance_config.models import ParentStage, Performance as PerformanceModel
from stage.asset import Asset, AssetType, AssignStages, DeleteMedia, UpdateMedia, UploadMedia
from config.project_globals import (DBSession, Base, metadata, engine, get_scoped_session,
                                    app, api, ScopedSession)
from utils import graphql_utils
from flask_graphql import GraphQLView
from asset.models import Stage as StageModel, StageAttribute as StageAttributeModel
from event_archive.models import Event as EventModel
from config.settings import VERSION
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene import relay
from graphql_relay.node.node import from_global_id
from sqlalchemy import desc
from user.models import ADMIN, SUPER_ADMIN
import graphene
import sys
import os
import json

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, '..'))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)


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


class Performance(SQLAlchemyObjectType):
    class Meta:
        model = PerformanceModel


class Stage(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")
    events = graphene.List(
        Event, description="Archived events of this performance", performance_id=graphene.Int())
    performances = graphene.List(
        Performance, description="Recorded performances")
    chats = graphene.List(
        Event, description="All chat sent by players and audiences")
    permission = graphene.String(description="Player access to this stage")
    media = graphene.List(Media, description="Media assigned to this stage")

    class Meta:
        model = StageModel
        model.db_id = model.id
        interfaces = (relay.Node,)
        connection_class = graphql_utils.CountableConnection

    def resolve_events(self, info, performance_id=None):
        events = DBSession.query(EventModel)\
            .filter(EventModel.performance_id == performance_id)\
            .filter(EventModel.topic.like("%/{}/%".format(self.file_location)))\
            .order_by(EventModel.mqtt_timestamp.asc())\
            .all()
        return events

    def resolve_performances(self, info):
        performances = DBSession.query(PerformanceModel).filter(
            PerformanceModel.stage_id == self.db_id).all()
        return performances

    def resolve_chats(self, info):
        events = DBSession.query(EventModel)\
            .filter(EventModel.topic.like("%/{}/chat".format(self.file_location)))\
            .order_by(EventModel.mqtt_timestamp.asc())\
            .all()
        return events

    def resolve_permission(self, info):
        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        if not user_id:
            return "audience"
        if self.owner_id == user_id:
            return 'owner'
        player_access = self.attributes.filter(
            StageAttributeModel.name == 'playerAccess').first()
        if player_access:
            accesses = json.loads(player_access.description)
            if len(accesses) == 2:
                if user_id in accesses[0]:
                    return "player"
                elif user_id in accesses[1]:
                    return "editor"
        return "audience"

    def resolve_media(self, info):
        return [{
            'id': x.child_asset.id,
            'name': x.child_asset.name,
            'type': x.child_asset.asset_type.name,
            'src': x.child_asset.file_location,
            'description': x.child_asset.description
        } for x in self.assets.all()]


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


class CreateStageInput(graphene.InputObjectType, StageAttribute):
    """Arguments to create a stage."""
    pass


class CreateStage(graphene.Mutation):
    """Mutation to create a stage."""
    stage = graphene.Field(
        lambda: Stage, description="Stage created by this mutation.")

    class Arguments:
        input = CreateStageInput(required=True)

    @jwt_required()
    def mutate(self, info, input):
        if not input.name or not input.file_location:
            raise Exception('Please fill in all required fields')

        data = graphql_utils.input_to_dictionary(input)

        stage = StageModel(**data)
        stage.owner_id = get_jwt_identity()
        # Add validation for non-empty passwords, etc.
        with ScopedSession() as local_db_session:
            local_db_session.add(stage)
            local_db_session.flush()
            stage_id = stage.id
            local_db_session.commit()

            stage = DBSession.query(StageModel).filter(
                StageModel.id == stage_id).first()
            return CreateStage(stage=stage)


class UpdateStageInput(graphene.InputObjectType, StageAttribute):
    id = graphene.ID(required=True, description="Global Id of the stage.")


class UpdateStage(graphene.Mutation):
    """Mutation to update a stage."""
    stage = graphene.Field(
        lambda: Stage, description="Stage updated by this mutation.")

    class Arguments:
        input = UpdateStageInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        with ScopedSession() as local_db_session:

            stage = local_db_session.query(StageModel).filter(
                StageModel.id == data['id']
            ).first()
            for key, value in data.items():
                if hasattr(stage, key):
                    setattr(stage, key, value)
                elif value:
                    attribute = stage.attributes.filter(
                        StageAttributeModel.name == key
                    ).first()
                    if attribute:
                        attribute.description = value
                    else:
                        attribute = StageAttributeModel(
                            stage_id=data['id'], name=key, description=value
                        )
                        local_db_session.add(attribute)

            local_db_session.commit()
            stage = DBSession.query(StageModel).filter(
                StageModel.id == data['id']).first()

            return UpdateStage(stage=stage)


class AssignMediaInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the stage.")
    media_ids = graphene.List(graphene.Int, description="Id of assigned media")


class AssignMedia(graphene.Mutation):
    """Mutation to update a stage."""
    stage = graphene.Field(
        lambda: Stage, description="Stage with assigned media")

    class Arguments:
        input = AssignMediaInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        with ScopedSession() as local_db_session:
            stage = local_db_session.query(StageModel).filter(
                StageModel.id == data['id']
            ).first()
            stage.assets.delete()
            for id in data['media_ids']:
                stage.assets.append(ParentStage(child_asset_id=id))

            local_db_session.commit()
            stage = DBSession.query(StageModel).filter(
                StageModel.id == data['id']).first()

            return AssignMedia(stage=stage)


class SweepStageInput(graphene.InputObjectType, StageAttribute):
    id = graphene.ID(required=True, description="Global Id of the stage.")


class SweepStage(graphene.Mutation):
    """Mutation to sweep a stage."""
    success = graphene.Boolean()
    performance_id = graphene.Int()

    class Arguments:
        input = SweepStageInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        with ScopedSession() as local_db_session:
            stage = local_db_session.query(StageModel)\
                .filter(StageModel.id == data['id'])\
                .first()

            events = DBSession.query(EventModel)\
                .filter(EventModel.performance_id == None)\
                .filter(EventModel.topic.like("%/{}/%".format(stage.file_location)))

            if events.count() > 0:
                performance = PerformanceModel(stage=stage)
                local_db_session.add(performance)
                local_db_session.flush()

                events.update(
                    {EventModel.performance_id: performance.id}, synchronize_session="fetch")
            else:
                raise Exception("The stage is already sweeped!")

            local_db_session.commit()

            return SweepStage(success=True, performance_id=performance.id)


class DeleteStage(graphene.Mutation):
    """Mutation to sweep a stage."""
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(
            required=True, description="Global Id of the stage to be deleted.")

    @jwt_required()
    def mutate(self, info, id):
        with ScopedSession() as local_db_session:
            id = from_global_id(id)[1]
            stage = local_db_session.query(StageModel).filter(
                StageModel.id == id).first()
            if stage:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == stage.owner_id:
                        raise Exception(
                            "Only stage owner or admin can delete this stage!")

                local_db_session.query(ParentStage).filter(
                    ParentStage.stage_id == id).delete(synchronize_session=False)
                local_db_session.query(StageAttributeModel).filter(
                    StageAttributeModel.stage_id == id).delete(synchronize_session=False)
                for performance in local_db_session.query(PerformanceModel).filter(
                        PerformanceModel.stage_id == id).all():
                    local_db_session.query(EventModel).filter(
                        EventModel.performance_id == performance.id).delete(synchronize_session=False)
                    local_db_session.delete(performance)
                local_db_session.delete(stage)
                local_db_session.flush()
                local_db_session.commit()
            else:
                raise Exception("Stage not found!")

        return DeleteStage(success=True)


class Mutation(graphene.ObjectType):
    createStage = CreateStage.Field()
    updateStage = UpdateStage.Field()
    sweepStage = SweepStage.Field()
    deleteStage = DeleteStage.Field()
    uploadMedia = UploadMedia.Field()
    updateMedia = UpdateMedia.Field()
    deleteMedia = DeleteMedia.Field()
    assignMedia = AssignMedia.Field()
    assignStages = AssignStages.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    stageList = StageConnectionField(
        Stage.connection, id=graphene.ID(), name_like=graphene.String(), file_location=graphene.String())
    assetList = StageConnectionField(
        Asset.connection, id=graphene.ID(), name_like=graphene.String(), asset_type=graphene.String())
    assetTypeList = StageConnectionField(
        AssetType.connection, id=graphene.ID(), name_like=graphene.String())


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stage_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f'/{VERSION}/stage_graphql/', view_func=GraphQLView.as_view(
        "stage_graphql", schema=stage_schema,
        graphiql=True
    )
)

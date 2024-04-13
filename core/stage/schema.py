# -*- coding: iso8859-15 -*-
import re
import graphene
import sys
import os
import json
import datetime

appdir = os.path.abspath(os.path.dirname(__file__))
projdir = os.path.abspath(os.path.join(appdir, "../.."))
if projdir not in sys.path:
    sys.path.append(appdir)
    sys.path.append(projdir)

from core.user.models import ADMIN, SUPER_ADMIN
from sqlalchemy import orm
from graphql_relay.node.node import from_global_id, to_global_id
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from config import PERFORMANCE_TOPIC_RULE, URL_PREFIX
from core.event_archive.models import Event as EventModel
from core.asset.models import Stage as StageModel, StageAttribute as StageAttributeModel
from flask_graphql import GraphQLView
from core.utils import graphql_utils
from core.project_globals import (
    DBSession,
    Base,
    metadata,
    engine,
    get_scoped_session,
    app,
    api,
    ScopedSession,
)
from core.stage.asset import (
    Asset,
    AssetConnectionField,
    AssetType,
    AssignStages,
    DeleteMedia,
    UpdateMedia,
    UploadMedia,
)
from core.performance_config.models import (
    ParentStage,
    Performance as PerformanceModel,
    Scene as SceneModel,
)
from flask_jwt_extended.view_decorators import jwt_required, verify_jwt_in_request
from flask_jwt_extended.utils import get_jwt_identity
from core.user.user_utils import current_user
from core.stage.scene import DeleteScene, SaveScene, Scene
from sqlalchemy.orm.session import make_transient
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from core.stage.performance import (
    Performance,
    DeletePerformance,
    SaveRecording,
    StartRecording,
    UpdatePerformance,
)


class StageAttribute:
    name = graphene.String(description="Stage Name")
    description = graphene.String(description="Stage Description")
    file_location = graphene.String(description="Unique File Location")
    status = graphene.String(description="Live/Rehearsal")
    visibility = graphene.Boolean(description="Show or hide the stage on the Foyer")
    cover = graphene.String(description="Cover image url")
    media = graphene.String(description="Media attached to stage")
    config = graphene.String(description="Stage configurations")
    playerAccess = graphene.String(
        description="Users who can access and edit this stage"
    )


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
        Event,
        description="Archived events of this performance",
        performance_id=graphene.Int(),
        cursor=graphene.Int(),
    )
    performances = graphene.List(Performance, description="Recorded performances")
    chats = graphene.List(Event, description="All chat sent by players and audiences")
    permission = graphene.String(description="Player access to this stage")
    media = graphene.List(Media, description="Media assigned to this stage")
    scenes = graphene.List(
        Scene, description="Saved stage scenes", performance_id=graphene.Int()
    )
    active_recording = graphene.Field(
        Performance, description="Current recording session"
    )

    class Meta:
        model = StageModel
        model.db_id = model.id
        interfaces = (relay.Node,)
        connection_class = graphql_utils.CountableConnection

    def resolve_db_id(self, info):
        return self.id

    def resolve_events(self, info, performance_id=None, cursor=0):
        events = (
            DBSession.query(EventModel)
            .filter(EventModel.performance_id == performance_id)
            .filter(EventModel.id > cursor)
            .filter(EventModel.topic.like("%/{}/%".format(self.file_location)))
            .order_by(EventModel.mqtt_timestamp.asc())
            .all()
        )
        return events

    def resolve_performances(self, info):
        performances = (
            DBSession.query(PerformanceModel)
            .filter(PerformanceModel.stage_id == self.db_id)
            .all()
        )
        return performances

    def resolve_chats(self, info):
        events = (
            DBSession.query(EventModel)
            .filter(EventModel.topic.like("%/{}/chat".format(self.file_location)))
            .order_by(EventModel.mqtt_timestamp.asc())
            .all()
        )
        return events

    def resolve_permission(self, info):
        result = verify_jwt_in_request(True)
        user_id = get_jwt_identity()
        if not user_id:
            return "audience"
        if self.owner_id == user_id:
            return "owner"
        player_access = self.attributes.filter(
            StageAttributeModel.name == "playerAccess"
        ).first()
        if player_access:
            accesses = json.loads(player_access.description)
            if len(accesses) == 2:
                if user_id in accesses[0]:
                    return "player"
                elif user_id in accesses[1]:
                    return "editor"
        return "audience"

    def resolve_media(self, info):
        return [
            {
                "id": x.child_asset.id,
                "name": x.child_asset.name,
                "type": x.child_asset.asset_type.name,
                "src": x.child_asset.file_location,
                "description": x.child_asset.description,
            }
            for x in self.assets.all()
        ]

    def resolve_scenes(self, info, performance_id=None):
        query = (
            DBSession.query(SceneModel)
            .filter(SceneModel.stage_id == self.db_id)
            .order_by(SceneModel.scene_order.asc())
        )
        if not performance_id:  # Only fetch disabled scene in performance replay
            query = query.filter(SceneModel.active == True)
        scenes = query.all()
        return scenes

    def resolve_active_recording(self, info):
        recording = (
            DBSession.query(PerformanceModel)
            .filter(PerformanceModel.stage_id == self.db_id)
            .filter(PerformanceModel.recording == True)
            .filter(PerformanceModel.saved_on == None)
            .first()
        )
        return recording


class FoyerStageConnectionField(SQLAlchemyConnectionField):
    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query: orm.Query = super(FoyerStageConnectionField, cls).get_query(
            model, info, sort, **args
        )
        query = query.filter(
            StageModel.attributes.any(name="visibility", description="true")
        )
        return query


class StageConnectionField(SQLAlchemyConnectionField):
    RELAY_ARGS = ["first", "last", "before", "after"]

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super(StageConnectionField, cls).get_query(model, info, sort, **args)
        for field, value in args.items():
            if field == "id":
                _type, _id = from_global_id(value)
                query = query.filter(getattr(model, field) == _id)
            elif field == "asset_type":
                query = query.filter(getattr(model, field).has(name=value))
            elif field == "permissions":
                return model.resolve_permission(info)
            elif len(field) > 5 and field[-4:] == "like":
                query = query.filter(getattr(model, field[:-5]).ilike(f"%{value}%"))
            elif field not in cls.RELAY_ARGS and hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
        return query


class CreateStageInput(graphene.InputObjectType, StageAttribute):
    """Arguments to create a stage."""

    pass


class CreateStage(graphene.Mutation):
    """Mutation to create a stage."""

    stage = graphene.Field(lambda: Stage, description="Stage created by this mutation.")

    class Arguments:
        input = CreateStageInput(required=True)

    @jwt_required()
    def mutate(self, info, input):
        if not input.name or not input.file_location:
            raise Exception("Please fill in all required fields")

        data = graphql_utils.input_to_dictionary(input)

        stage = StageModel(**data)
        stage.owner_id = get_jwt_identity()
        # Add validation for non-empty passwords, etc.
        with ScopedSession() as local_db_session:
            local_db_session.add(stage)
            local_db_session.flush()
            stage_id = stage.id
            local_db_session.commit()

            stage = (
                DBSession.query(StageModel).filter(StageModel.id == stage_id).first()
            )
            return CreateStage(stage=stage)


class UpdateStageInput(graphene.InputObjectType, StageAttribute):
    id = graphene.ID(required=True, description="Global Id of the stage.")


class UpdateStage(graphene.Mutation):
    """Mutation to update a stage."""

    stage = graphene.Field(lambda: Stage, description="Stage updated by this mutation.")

    class Arguments:
        input = UpdateStageInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageModel)
                .filter(StageModel.id == data["id"])
                .first()
            )
            mapper = inspect(StageModel)
            attributes = mapper.attrs.keys()

            for key, value in data.items():
                if key == "file_location":
                    continue
                if (
                    hasattr(stage, key)
                    and key in attributes
                    and not isinstance(mapper.attrs[key], hybrid_property)
                ):
                    setattr(stage, key, value)
                elif value != None:
                    if not value:
                        value = ""
                    attribute = stage.attributes.filter(
                        StageAttributeModel.name == key
                    ).first()
                    if attribute:
                        attribute.description = value
                    else:
                        attribute = StageAttributeModel(
                            stage_id=data["id"], name=key, description=value
                        )
                        local_db_session.add(attribute)

            local_db_session.commit()
            stage = (
                DBSession.query(StageModel).filter(StageModel.id == data["id"]).first()
            )

            return UpdateStage(stage=stage)


class UpdateAttributeStatus(graphene.Mutation):
    """Mutation to update a stage status attribute."""

    result = graphene.String()

    class Arguments:
        stage_id = graphene.ID(required=True, description="Global Id of the stage.")

    # decorate this with jwt login decorator.
    def mutate(self, info, stage_id):
        with ScopedSession() as local_db_session:
            _id = int(from_global_id(stage_id)[1])
            attribute = (
                local_db_session.query(StageAttributeModel)
                .filter(
                    StageAttributeModel.stage_id == _id,
                    StageAttributeModel.name == "status",
                )
                .first()
            )
            if attribute is not None:
                attribute.description = (
                    "rehearsal" if attribute.description == "live" else "live"
                )
            else:
                attribute = StageAttributeModel(
                    stage_id=_id, name="status", description="live"
                )
            local_db_session.add(attribute)
            local_db_session.commit()

            return UpdateAttributeStatus(result=attribute.description)


class UpdateAttributeVisibility(graphene.Mutation):
    """Mutation to update a stage visibility attribute."""

    result = graphene.String()

    class Arguments:
        stage_id = graphene.ID(required=True, description="Global Id of the stage.")

    # decorate this with jwt login decorator.
    def mutate(self, info, stage_id):
        with ScopedSession() as local_db_session:
            _id = int(from_global_id(stage_id)[1])
            attribute = (
                local_db_session.query(StageAttributeModel)
                .filter(
                    StageAttributeModel.stage_id == _id,
                    StageAttributeModel.name == "visibility",
                )
                .first()
            )
            if attribute is not None:
                attribute.description = True if not attribute.description else ""
            else:
                attribute = StageAttributeModel(
                    stage_id=_id, name="visibility", description=True
                )
            local_db_session.add(attribute)
            local_db_session.commit()
            return UpdateAttributeVisibility(result=attribute.description)


class UpdateLastAccess(graphene.Mutation):
    """Mutation to update a stage last access attribute."""

    result = graphene.String()

    class Arguments:
        stage_id = graphene.ID(required=True, description="Global Id of the stage.")

    # decorate this with jwt login decorator.
    def mutate(self, info, stage_id):
        with ScopedSession() as local_db_session:
            _id = int(stage_id)
            stage = local_db_session.query(StageModel).filter(StageModel.id == _id)
            if stage:
                stage.update(
                    {StageModel.last_access: datetime.datetime.utcnow()},
                    synchronize_session="fetch",
                )

            local_db_session.commit()
            return UpdateLastAccess(result=datetime.datetime.utcnow())


class AssignMediaInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the stage.")
    media_ids = graphene.List(graphene.Int, description="Id of assigned media")


class AssignMedia(graphene.Mutation):
    """Mutation to update a stage."""

    stage = graphene.Field(lambda: Stage, description="Stage with assigned media")

    class Arguments:
        input = AssignMediaInput(required=True)

    # decorate this with jwt login decorator.
    def mutate(self, info, input):
        data = graphql_utils.input_to_dictionary(input)
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageModel)
                .filter(StageModel.id == data["id"])
                .first()
            )
            stage.assets.delete()
            for id in data["media_ids"]:
                stage.assets.append(ParentStage(child_asset_id=id))

            local_db_session.commit()
            stage = (
                DBSession.query(StageModel).filter(StageModel.id == data["id"]).first()
            )

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
            stage = (
                local_db_session.query(StageModel)
                .filter(StageModel.id == data["id"])
                .first()
            )

            events = (
                DBSession.query(EventModel)
                .filter(EventModel.performance_id == None)
                .filter(EventModel.topic.like("%/{}/%".format(stage.file_location)))
            )

            if events.count() > 0:
                performance = PerformanceModel(stage=stage)
                local_db_session.add(performance)
                local_db_session.flush()

                events.update(
                    {EventModel.performance_id: performance.id},
                    synchronize_session="fetch",
                )
            else:
                raise Exception("The stage is already sweeped!")

            local_db_session.commit()

            return SweepStage(success=True, performance_id=performance.id)


class DeleteStage(graphene.Mutation):
    """Mutation to delete a stage."""

    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(
            required=True, description="Global Id of the stage to be deleted."
        )

    @jwt_required()
    def mutate(self, info, id):
        with ScopedSession() as local_db_session:
            id = from_global_id(id)[1]
            stage = (
                local_db_session.query(StageModel).filter(StageModel.id == id).first()
            )
            if stage:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == stage.owner_id:
                        raise Exception(
                            "Only stage owner or admin can delete this stage!"
                        )

                local_db_session.query(ParentStage).filter(
                    ParentStage.stage_id == id
                ).delete(synchronize_session=False)
                local_db_session.query(StageAttributeModel).filter(
                    StageAttributeModel.stage_id == id
                ).delete(synchronize_session=False)
                local_db_session.query(SceneModel).filter(
                    SceneModel.stage_id == id
                ).delete(synchronize_session=False)

                for performance in (
                    local_db_session.query(PerformanceModel)
                    .filter(PerformanceModel.stage_id == id)
                    .all()
                ):
                    local_db_session.query(EventModel).filter(
                        EventModel.performance_id == performance.id
                    ).delete(synchronize_session=False)
                    local_db_session.delete(performance)
                topic_prefix = PERFORMANCE_TOPIC_RULE.replace("#", stage.file_location)
                local_db_session.query(EventModel).filter(
                    EventModel.topic.startswith(topic_prefix)
                ).delete(synchronize_session=False)
                local_db_session.delete(stage)
                local_db_session.flush()
                local_db_session.commit()
            else:
                raise Exception("Stage not found!")

        return DeleteStage(success=True)


class DuplicateStage(graphene.Mutation):
    """Mutation to duplicate a stage."""

    success = graphene.Boolean()
    new_stage_id = graphene.ID()

    class Arguments:
        id = graphene.ID(
            required=True, description="Global Id of the stage to be duplicated."
        )
        name = graphene.String(
            required=True, description="New name of the duplicated stage"
        )

    @jwt_required()
    def mutate(self, info, id, name):
        with ScopedSession() as local_db_session:
            code, error, user, timezone = current_user()
            id = from_global_id(id)[1]
            stage = (
                local_db_session.query(StageModel).filter(StageModel.id == id).first()
            )
            if stage:
                local_db_session.expunge(stage)
                make_transient(stage)
                original_stage_id = id
                stage.id = None
                stage.name = name
                stage.owner_id = user.id
                stage.last_access = None
                stage.created_on = datetime.datetime.utcnow()
                shortname = re.sub(
                    "\s+", "-", re.sub("[^A-Za-z0-9 ]+", "", name)
                ).lower()

                suffix = ""
                while True:
                    existedStages = (
                        DBSession.query(StageModel)
                        .filter(StageModel.file_location == f"{shortname}{suffix}")
                        .first()
                    )
                    if existedStages:
                        suffix = int(suffix or 0) + 1
                    else:
                        break
                stage.file_location = f"{shortname}{suffix}"
                local_db_session.add(stage)
                local_db_session.flush()
                new_stage_id = stage.id

                # Clone media and attributes, player accesses,...
                for ps in (
                    local_db_session.query(ParentStage)
                    .filter(ParentStage.stage_id == original_stage_id)
                    .all()
                ):
                    local_db_session.add(
                        ParentStage(
                            stage_id=new_stage_id, child_asset_id=ps.child_asset_id
                        )
                    )
                for attribute in (
                    local_db_session.query(StageAttributeModel)
                    .filter(StageAttributeModel.stage_id == original_stage_id)
                    .all()
                ):
                    local_db_session.add(
                        StageAttributeModel(
                            stage_id=new_stage_id,
                            name=attribute.name,
                            description=attribute.description,
                        )
                    )
                local_db_session.flush()
                local_db_session.commit()
                return DuplicateStage(
                    success=True, new_stage_id=to_global_id("Stage", new_stage_id)
                )
            else:
                raise Exception("Stage not found!")


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
    saveScene = SaveScene.Field()
    deleteScene = DeleteScene.Field()
    duplicateStage = DuplicateStage.Field()
    updatePerformance = UpdatePerformance.Field()
    deletePerformance = DeletePerformance.Field()
    startRecording = StartRecording.Field()
    saveRecording = SaveRecording.Field()
    updateStatus = UpdateAttributeStatus.Field()
    updateVisibility = UpdateAttributeVisibility.Field()
    updateLastAccess = UpdateLastAccess.Field()


class Query(graphene.ObjectType):
    code, error, user, timezone = current_user()
    node = relay.Node.Field()
    foyerStageList = FoyerStageConnectionField(Stage.connection)
    if user.role in (ADMIN, SUPER_ADMIN):
        stageList = StageConnectionField(
            Stage.connection,
            id=graphene.ID(),
            name_like=graphene.String(),
            file_location=graphene.String(),
            created_on=graphene.DateTime(),
        )
    else:
        stageList = StageConnectionField(
            Stage.connection,
            id=graphene.ID(),
            name_like=graphene.String(),
            file_location=graphene.String(),
            created_on=graphene.DateTime(),
            permissions in ('owner','player','editor'),
        )
    assetList = AssetConnectionField(
        Asset.connection,
        id=graphene.ID(),
        name_like=graphene.String(),
        asset_type=graphene.String(),
        file_location=graphene.String(),
    )
    assetTypeList = StageConnectionField(
        AssetType.connection, id=graphene.ID(), name_like=graphene.String()
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
stage_schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule(
    f"/{URL_PREFIX}stage_graphql/",
    view_func=GraphQLView.as_view("stage_graphql", schema=stage_schema, graphiql=True),
)

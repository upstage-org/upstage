from asset.models import Stage
import os
from user.models import ADMIN, SUPER_ADMIN
from user.user_utils import current_user
from config.project_globals import appdir, ScopedSession
from performance_config.models import ParentStage, Performance as PerformanceModel
from event_archive.models import Event
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql_relay.node.node import from_global_id
import graphene
from flask_jwt_extended import jwt_required, get_jwt_identity

absolutePath = os.path.dirname(appdir)
storagePath = 'ui/static/assets'


class Performance(SQLAlchemyObjectType):
    class Meta:
        model = PerformanceModel


class UpdatePerformance(graphene.Mutation):
    """Mutation to update performance information"""
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True, description="Performance id")
        name = graphene.String(
            description="New name of the performance", required=False)
        description = graphene.String(
            description="New description of the performance", required=False)

    @jwt_required()
    def mutate(self, info, id, name=None, description=None):
        if not name:
            raise Exception("Please pick a name!")

        current_user_id = get_jwt_identity()
        with ScopedSession() as local_db_session:
            performance = local_db_session.query(PerformanceModel).filter(
                PerformanceModel.id == id).first()
            if performance:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == performance.stage.owner_id:
                        raise Exception(
                            "Only stage owner or Admin can update archived performance information!")

                performance.name = name
                performance.description = description
                local_db_session.flush()
                local_db_session.commit()
            else:
                raise Exception("Performance not found!")

            return UpdatePerformance(success=True)


class DeletePerformance(graphene.Mutation):
    """Mutation to delete a performance."""
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(
            required=True, description="ID of the performance to be deleted.")

    @jwt_required()
    def mutate(self, info, id):
        with ScopedSession() as local_db_session:
            performance = local_db_session.query(PerformanceModel).filter(
                PerformanceModel.id == id).first()
            if performance:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == performance.owner_id:
                        raise Exception(
                            "Only stage owner or Admin can delete this performance!")

                local_db_session.query(Event).filter(
                    Event.performance_id == id).delete(synchronize_session=False)
                local_db_session.delete(performance)
                local_db_session.flush()
                local_db_session.commit()
            else:
                raise Exception("Performance not found!")

        return DeletePerformance(success=True)


class StartRecording(graphene.Mutation):
    """Mutation to create a recording performance"""
    performance = graphene.Field(
        lambda: Performance, description="Performance created by this mutation.")

    class Arguments:
        stage_id = graphene.ID(required=True, description="Stage id")
        name = graphene.String(
            description="New name of the performance", required=False)
        description = graphene.String(
            description="New description of the performance", required=False)

    @jwt_required()
    def mutate(self, info, stage_id, name=None, description=None):
        if not name:
            raise Exception("Please pick a name!")

        current_user_id = get_jwt_identity()
        with ScopedSession() as local_db_session:
            id = from_global_id(stage_id)[1]
            stage = local_db_session.query(
                Stage).filter(Stage.id == id).first()

            if stage:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == stage.owner_id:
                        raise Exception(
                            "Only stage owner or Admin can start a recording on this stage!")
            else:
                raise Exception("Stage does not exist!")

            performance = PerformanceModel(
                stage=stage, name=name, description=description, recording=True)
            local_db_session.add(performance)
            local_db_session.flush()
            local_db_session.commit()

            performance = local_db_session.query(PerformanceModel).filter(
                PerformanceModel.id == performance.id).first()
            return StartRecording(performance=performance)

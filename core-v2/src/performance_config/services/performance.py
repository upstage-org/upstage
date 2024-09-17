from datetime import datetime
from graphql import GraphQLError
from config.database import DBSession, ScopedSession
from core.helpers.object import convert_keys_to_camel_case
from event_archive.entities.event import EventEntity
from performance_config.entities.performance import PerformanceEntity
from stages.entities.stage import StageEntity
from stages.http.validation import PerformanceInput, RecordInput
from users.entities.user import ADMIN, SUPER_ADMIN, UserEntity
from sqlalchemy.orm.session import make_transient


class PerformanceService:
    def __init__(self):
        pass

    def create_performance(self, user: UserEntity, input: RecordInput):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity).filter_by(id=input.stageId).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            if user.role not in ["SUPER_ADMIN", "ADMIN"] and user.id != stage.owner_id:
                raise GraphQLError("You are not allowed to record for this stage")

            performance = PerformanceEntity(
                name=input.name,
                description=input.description,
                recording=True,
                stage_id=input.stageId,
            )

            local_db_session.add(performance)
            local_db_session.flush()
            local_db_session.commit()
            performance = DBSession.query(PerformanceEntity).filter_by(id=performance.id).first()
            return convert_keys_to_camel_case(performance)

    def update_performance(self, user: UserEntity, input: PerformanceInput):
        with ScopedSession() as local_db_session:
            performance = (
                local_db_session.query(PerformanceEntity).filter_by(id=input.id).first()
            )
            if not performance:
                raise GraphQLError("Performance not found")

            if (
                user.role not in ["SUPER_ADMIN", "ADMIN"]
                and user.id != performance.owner_id
            ):
                raise GraphQLError("You are not allowed to update this performance")

            performance.name = input.name
            performance.description = input.description
            local_db_session.flush()
            local_db_session.commit()
            return {"success": True}

    def delete_performance(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            performance = (
                local_db_session.query(PerformanceEntity).filter_by(id=id).first()
            )
            if not performance:
                raise GraphQLError("Performance not found")

            if (
                user.role not in ["SUPER_ADMIN", "ADMIN"]
                and user.id != performance.stage.owner_id
            ):
                raise GraphQLError("You are not allowed to delete this performance")

            local_db_session.query(EventEntity).filter(
                EventEntity.performance_id == id
            ).delete(synchronize_session=False)
            local_db_session.delete(performance)
            local_db_session.commit()
            return {"success": True}

    def save_recording(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            performance = (
                local_db_session.query(PerformanceEntity).filter_by(id=id).first()
            )
            if not performance:
                raise GraphQLError("Performance not found")

            if (
                user.role not in [SUPER_ADMIN, ADMIN]
                and user.id != performance.owner_id
            ):
                raise GraphQLError("Only stage owner or Admin can save a recording!")
            saved_on = datetime.now()

            events = (
                local_db_session.query(EventEntity)
                .filter(
                    EventEntity.topic.ilike(
                        "%/{}/%".format(performance.stage.file_location)
                    )
                )
                .filter(EventEntity.created > performance.created_on)
                .filter(EventEntity.created < saved_on)
            )

            if events.count() > 0:
                for event in events.all():
                    local_db_session.expunge(event)
                    make_transient(event)
                    event.id = None
                    event.performance_id = performance.id
                    local_db_session.add(event)
            else:
                raise GraphQLError("Nothing to record!")

            performance.saved_on = saved_on
            performance.recording = False
            local_db_session.flush()
            local_db_session.commit()
            return performance

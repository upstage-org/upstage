from datetime import datetime
from graphql import GraphQLError
from global_config import DBSession, ScopedSession, convert_keys_to_camel_case
from event_archive.db_models.event import EventModel
from performance_config.db_models.performance import PerformanceModel
from performance_config.db_models.performance_mqtt_config import (
    PerformanceMQTTConfigModel,
)
from performance_config.db_models.performance_config import PerformanceConfigModel
from stages.db_models.stage import StageModel
from stages.http.validation import PerformanceInput, RecordInput
from users.db_models.user import ADMIN, SUPER_ADMIN, UserModel
from sqlalchemy.orm.session import make_transient


class PerformanceService:
    def __init__(self):
        pass

    def get_performance_communication(self):
        return [
            convert_keys_to_camel_case(performance.to_dict())
            for performance in DBSession.query(PerformanceMQTTConfigModel).all()
        ]

    def get_performance_config(self):
        return [
            convert_keys_to_camel_case(performance.to_dict())
            for performance in DBSession.query(PerformanceConfigModel).all()
        ]

    def create_performance(self, user: UserModel, input: RecordInput):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageModel).filter_by(id=input.stageId).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            if user.role not in [SUPER_ADMIN, ADMIN] and user.id != stage.owner_id:
                raise GraphQLError("You are not allowed to record for this stage")

            performance = PerformanceModel(
                name=input.name,
                description=input.description,
                recording=True,
                stage_id=input.stageId,
            )

            local_db_session.add(performance)
            local_db_session.commit()
            local_db_session.flush()
            performance = (
                DBSession.query(PerformanceModel).filter_by(id=performance.id).first()
            )
            return convert_keys_to_camel_case(performance)

    def update_performance(self, user: UserModel, input: PerformanceInput):
        with ScopedSession() as local_db_session:
            performance = (
                local_db_session.query(PerformanceModel).filter_by(id=input.id).first()
            )

            if not performance:
                raise GraphQLError("Performance not found")

            if (
                user.role not in [SUPER_ADMIN, ADMIN]
                and user.id != performance.stage.owner_id
            ):
                raise GraphQLError("You are not allowed to update this performance")

            performance.name = input.name
            performance.description = input.description
            local_db_session.flush()

            return {"success": True}

    def delete_performance(self, user: UserModel, id: int):
        with ScopedSession() as local_db_session:
            performance = (
                local_db_session.query(PerformanceModel).filter_by(id=id).first()
            )
            if not performance:
                raise GraphQLError("Performance not found")

            if (
                user.role not in [SUPER_ADMIN, ADMIN]
                and user.id != performance.stage.owner_id
            ):
                raise GraphQLError("You are not allowed to delete this performance")

            local_db_session.query(EventModel).filter(
                EventModel.performance_id == id
            ).delete(synchronize_session=False)
            local_db_session.delete(performance)
            return {"success": True}

    def save_recording(self, user: UserModel, id: int):
        with ScopedSession() as local_db_session:
            performance = (
                local_db_session.query(PerformanceModel).filter_by(id=id).first()
            )
            if not performance:
                raise GraphQLError("Performance not found")

            if (
                user.role not in [SUPER_ADMIN, ADMIN]
                and user.id != performance.stage.owner_id
            ):
                raise GraphQLError("Only stage owner or Admin can save a recording!")
            saved_on = datetime.now()

            events = (
                local_db_session.query(EventModel)
                .filter(
                    EventModel.topic.ilike(
                        "%/{}/%".format(performance.stage.file_location)
                    )
                )
                .filter(EventModel.created > performance.created_on)
                .filter(EventModel.created < saved_on)
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

            return (
                DBSession.query(PerformanceModel)
                .filter_by(id=performance.id)
                .first()
                .to_dict()
            )

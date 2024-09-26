from datetime import datetime
import re
from graphql import GraphQLError
from sqlalchemy import and_
from config.database import DBSession, ScopedSession
from core.helpers.object import convert_keys_to_camel_case
from event_archive.entities.event import EventEntity
from performance_config.entities.performance import PerformanceEntity
from performance_config.entities.scene import SceneEntity
from stages.entities.parent_stage import ParentStageEntity
from stages.entities.stage import StageEntity
from stages.entities.stage_attribute import StageAttributeEntity
from stages.http.validation import DuplicateStageInput, StageInput
from users.entities.user import ADMIN, SUPER_ADMIN, UserEntity


class StageService:
    def __init__(self):
        pass

    def create_stage(self, user: UserEntity, input: StageInput):
        with ScopedSession() as local_db_session:
            stage = StageEntity(
                name=input.name,
                description=input.description,
                owner_id=user.id,
                file_location=input.fileLocation,
            )

            local_db_session.add(stage)
            local_db_session.commit()

            local_db_session.refresh(stage)
            self.update_stage_attribute(
                stage.id, "cover", input.cover, local_db_session
            )
            self.update_stage_attribute(
                stage.id, "visibility", str(input.visibility), local_db_session
            )
            self.update_stage_attribute(
                stage.id, "description", input.description, local_db_session
            )
            self.update_stage_attribute(
                stage.id, "status", input.status, local_db_session
            )
            self.update_stage_attribute(
                stage.id, "playerAccess", input.playerAccess, local_db_session
            )
            local_db_session.commit()
            local_db_session.flush()
            return convert_keys_to_camel_case(stage.to_dict())

    def update_stage(self, user: UserEntity, input: StageInput):
        with ScopedSession() as local_db_session:
            stage = local_db_session.query(StageEntity).filter_by(id=input.id).first()
            if not stage or not input.id:
                raise GraphQLError("Stage not found")

            stage.name = input.name
            stage.description = input.description
            stage.file_location = input.fileLocation
            self.update_stage_attribute(
                stage.id, "cover", input.cover, local_db_session
            )
            self.update_stage_attribute(
                stage.id, "visibility", str(input.visibility), local_db_session
            )
            self.update_stage_attribute(
                stage.id, "description", input.description, local_db_session
            )
            self.update_stage_attribute(
                stage.id, "status", input.status, local_db_session
            )
            self.update_stage_attribute(
                stage.id, "playerAccess", input.playerAccess, local_db_session
            )

            self.update_stage_attribute(
                stage.id, "config", input.config, local_db_session
            )
            local_db_session.commit()
            return convert_keys_to_camel_case(stage.to_dict())

    def update_stage_attribute(
        self, stage_id: int, name: str, value: str, local_db_session
    ):
        if not value:
            return

        if stage_id:
            stage_attribute = (
                local_db_session.query(StageAttributeEntity)
                .filter(
                    and_(
                        StageAttributeEntity.stage_id == stage_id,
                        StageAttributeEntity.name == name,
                    )
                )
                .first()
            )
            if stage_attribute:
                stage_attribute.description = value
                local_db_session.commit()
                return
        local_db_session.add(
            StageAttributeEntity(stage_id=stage_id, name=name, description=value)
        )

    def delete_stage(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity).filter(StageEntity.id == id).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            if stage.owner_id != user.id and user.role not in [ADMIN, SUPER_ADMIN]:
                raise GraphQLError("You are not authorized to delete this stage")

            local_db_session.query(StageAttributeEntity).filter(
                StageAttributeEntity.stage_id == id
            ).delete()
            local_db_session.query(ParentStageEntity).filter(
                ParentStageEntity.stage_id == id
            ).delete()

            local_db_session.query(SceneEntity).filter(
                SceneEntity.stage_id == id
            ).delete()

            performances = local_db_session.query(PerformanceEntity).filter(
                PerformanceEntity.stage_id == id
            )

            local_db_session.query(EventEntity).filter(
                EventEntity.performance_id.in_([p.id for p in performances])
            ).delete()

            local_db_session.query(PerformanceEntity).filter(
                PerformanceEntity.stage_id == id
            )

            local_db_session.delete(stage)
            local_db_session.commit()
            local_db_session.flush()
            return {"success": True, "message": "Stage deleted"}

    def duplicate_stage(self, user: UserEntity, input: DuplicateStageInput):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity)
                .filter(StageEntity.id == input.id)
                .first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            file_location = self.get_short_name(input.name, local_db_session)

            new_stage = StageEntity(
                name=input.name,
                description=stage.description,
                owner_id=user.id,
                file_location=file_location,
            )

            local_db_session.add(new_stage)
            local_db_session.commit()
            local_db_session.refresh(new_stage)

            self.copy_data(input, local_db_session, new_stage)

            local_db_session.commit()
            local_db_session.flush()
            return convert_keys_to_camel_case(new_stage.to_dict())

    def copy_data(
        self, input: DuplicateStageInput, local_db_session, new_stage: StageEntity
    ):
        stage_attributes = (
            local_db_session.query(StageAttributeEntity)
            .filter(StageAttributeEntity.stage_id == input.id)
            .all()
        )

        for stage_attribute in stage_attributes:
            self.update_stage_attribute(
                new_stage.id,
                stage_attribute.name,
                stage_attribute.description,
                local_db_session,
            )

        parent_stages = (
            local_db_session.query(ParentStageEntity)
            .filter(ParentStageEntity.stage_id == input.id)
            .all()
        )
        for parent_stage in parent_stages:
            local_db_session.add(
                ParentStageEntity(
                    stage_id=new_stage.id,
                    child_asset_id=parent_stage.child_asset_id,
                )
            )

    def get_short_name(self, name, local_db_session):
        shortname = re.sub(r"\s+", "-", re.sub("[^A-Za-z0-9 ]+", "", name)).lower()

        suffix = ""
        while True:
            existed_stage = (
                local_db_session.query(StageEntity)
                .filter(StageEntity.file_location == f"{shortname}{suffix}")
                .first()
            )
            if existed_stage:
                suffix = int(suffix or 0) + 1
            else:
                break
        return f"{shortname}{suffix}"

    def sweep_stage(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity).filter(StageEntity.id == id).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            events = (
                local_db_session.query(EventEntity)
                .filter(EventEntity.performance_id == None)
                .filter(EventEntity.topic.ilike("%/{}/%".format(stage.file_location)))
            )

            if events.count() > 0:
                performance = PerformanceEntity(stage_id=stage.id)

                local_db_session.add(performance)
                local_db_session.flush()

                events.update(
                    {EventEntity.performance_id: performance.id},
                    synchronize_session="fetch",
                )
            else:
                raise GraphQLError("The stage is already sweeped!")

            local_db_session.commit()

            return convert_keys_to_camel_case(
                {"success": True, "performanceId": performance.id}
            )

    def update_status(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity).filter(StageEntity.id == id).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            if stage.owner_id != user.id and user.role not in [ADMIN, SUPER_ADMIN]:
                raise GraphQLError("You are not authorized to update this stage")

            attribute = (
                local_db_session.query(StageAttributeEntity)
                .filter(
                    StageAttributeEntity.stage_id == id,
                    StageAttributeEntity.name == "status",
                )
                .first()
            )

            if attribute is not None:
                attribute.description = (
                    "rehearsal" if attribute.description == "live" else "live"
                )
            else:
                attribute = StageAttributeEntity(
                    stage_id=id, name="status", description="live"
                )
            local_db_session.add(attribute)
            local_db_session.commit()
            return {"result": attribute.description}

    def update_visibility(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity).filter(StageEntity.id == id).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            if stage.owner_id != user.id and user.role not in [ADMIN, SUPER_ADMIN]:
                raise GraphQLError("You are not authorized to update this stage")

            attribute = (
                local_db_session.query(StageAttributeEntity)
                .filter(
                    StageAttributeEntity.stage_id == id,
                    StageAttributeEntity.name == "visibility",
                )
                .first()
            )

            if attribute is not None:
                attribute.description = True if not attribute.description else ""
            else:
                attribute = StageAttributeEntity(
                    stage_id=id, name="visibility", description=True
                )
            local_db_session.add(attribute)
            local_db_session.commit()
            return {"result": attribute.description}

    def update_last_access(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            stage = (
                local_db_session.query(StageEntity).filter(StageEntity.id == id).first()
            )
            if not stage:
                raise GraphQLError("Stage not found")

            if stage.owner_id != user.id and user.role not in [ADMIN, SUPER_ADMIN]:
                raise GraphQLError("You are not authorized to update this stage")

            stage.last_access = datetime.now()
            local_db_session.commit()
            return {"result": stage.last_access}

    def get_parent_stage(self):
        return [
            convert_keys_to_camel_case(stage)
            for stage in DBSession.query(ParentStageEntity).all()
        ]
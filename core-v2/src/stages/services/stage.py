from config.database import ScopedSession
from core.helpers.object import convert_keys_to_camel_case
from stages.entities.stage import StageEntity
from stages.entities.stage_attribute import StageAttributeEntity
from stages.http.validation import StageInput
from users.entities.user import UserEntity


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
            local_db_session.add(
                StageAttributeEntity(
                    stage_id=stage.id, name="cover", description=input.cover
                )
            )
            local_db_session.add(
                StageAttributeEntity(
                    stage_id=stage.id,
                    name="visibility",
                    description=str(input.visibility),
                )
            )
            local_db_session.add(
                StageAttributeEntity(
                    stage_id=stage.id, name="description", description=input.description
                )
            )
            local_db_session.add(
                StageAttributeEntity(
                    stage_id=stage.id, name="status", description=input.status
                )
            )
            local_db_session.add(
                StageAttributeEntity(
                    stage_id=stage.id,
                    name="playerAccess",
                    description=input.playerAccess,
                )
            )
            local_db_session.commit()

            return convert_keys_to_camel_case(stage.to_dict())

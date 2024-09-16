from graphql import GraphQLError
from config.database import ScopedSession
from core.helpers.object import convert_keys_to_camel_case
from performance_config.entities.scene import SceneEntity
from stages.http.validation import SceneInput
from users.entities.user import ADMIN, SUPER_ADMIN, UserEntity


class SceneService:
    def __init__(self):
        pass

    def create_scene(self, user: UserEntity, input: SceneInput):
        with ScopedSession() as local_db_session:
            scene = SceneEntity(
                owner_id=user.id,
                stage_id=input.stageId,
                payload=input.payload,
                scene_preview=input.preview,
            )

            scene_order = (
                local_db_session.query(SceneEntity)
                .filter(SceneEntity.stage_id == input.stageId)
                .count()
                + 1
            )

            scene.scene_order = scene_order

            if input.name:
                existed_scene = (
                    local_db_session.query(SceneEntity)
                    .filter(SceneEntity.stage_id == stage_id)
                    .filter(SceneEntity.active == True)
                    .filter(SceneEntity.name == input.name)
                    .first()
                )
                if existed_scene:
                    raise GraphQLError(
                        'Scene "{}" already existed. Please choose another name!'.format(
                            input.name
                        )
                    )
                scene.name = input.name
            else:
                scene.name = f"Scene {scene_order}"

            local_db_session.add(scene)
            local_db_session.flush()
            local_db_session.commit()
            local_db_session.refresh(scene)
            return convert_keys_to_camel_case(scene)

    def delete_scene(self, user: UserEntity, id: int):
        with ScopedSession() as local_db_session:
            scene = local_db_session.query(SceneEntity).filter_by(id=id).first()
            if not scene:
                raise GraphQLError("Scene not found")

            if user.role not in [SUPER_ADMIN, ADMIN] and scene.owner_id != user.id:
                return {
                    "success": False,
                    "message": "You are not allowed to delete this scene",
                }

            scene.active = False
            local_db_session.flush()
            local_db_session.commit()
            return {"success": True, "message": "Scene deleted successfully"}

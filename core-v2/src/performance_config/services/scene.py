from graphql import GraphQLError
from global_config import ScopedSession, convert_keys_to_camel_case
from performance_config.db_models.scene import SceneModel
from stages.http.validation import SceneInput
from users.db_models.user import ADMIN, SUPER_ADMIN, UserModel


class SceneService:
    def __init__(self):
        pass

    def get_scene(self):
        return [
            convert_keys_to_camel_case(scene)
            for scene in ScopedSession.query(SceneModel).all()
        ]

    def create_scene(self, user: UserModel, input: SceneInput):
        with ScopedSession() as local_db_session:
            scene = SceneModel(
                owner_id=user.id,
                stage_id=input.stageId,
                payload=input.payload,
                scene_preview=input.preview,
            )

            scene_order = (
                local_db_session.query(SceneModel)
                .filter(SceneModel.stage_id == input.stageId)
                .count()
                + 1
            )

            scene.scene_order = scene_order

            if input.name:
                existed_scene = (
                    local_db_session.query(SceneModel)
                    .filter(SceneModel.stage_id == input.stageId)
                    .filter(SceneModel.active == True)
                    .filter(SceneModel.name == input.name)
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

    def delete_scene(self, user: UserModel, id: int):
        with ScopedSession() as local_db_session:
            scene = local_db_session.query(SceneModel).filter_by(id=id).first()
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

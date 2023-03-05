import os
from core.user.models import ADMIN, SUPER_ADMIN
from core.user.user_utils import current_user
from core.project_globals import appdir, ScopedSession
from core.performance_config.models import Scene as SceneModel
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql_relay.node.node import from_global_id
import graphene
from flask_jwt_extended import jwt_required, get_jwt_identity

absolutePath = os.path.dirname(appdir)
storagePath = "uploads/assets"


class Scene(SQLAlchemyObjectType):
    db_id = graphene.Int(description="Database ID")

    class Meta:
        model = SceneModel
        model.db_id = model.id


class SaveScene(graphene.Mutation):
    """Mutation to save a snapshot of a stage to a scene."""

    id = graphene.Int(description="ID of the the new scene that was created")

    class Arguments:
        stage_id = graphene.Int(required=True, description="Name of the media")
        payload = graphene.String(description="JSON serialized snapshot of the stage")
        preview = graphene.String(
            description="Base64 encoded preview image of the scene", default_value=None
        )
        name = graphene.String(description="Name of the scene", required=False)

    @jwt_required()
    def mutate(self, info, stage_id, payload, preview, name=None):
        current_user_id = get_jwt_identity()
        with ScopedSession() as local_db_session:
            scene = SceneModel(
                owner_id=current_user_id,
                stage_id=stage_id,
                payload=payload,
                scene_preview=preview,
            )
            scene_order = (
                local_db_session.query(SceneModel)
                .filter(SceneModel.stage_id == stage_id)
                .count()
                + 1
            )
            scene.scene_order = scene_order
            if name:
                existedScene = (
                    local_db_session.query(SceneModel)
                    .filter(SceneModel.stage_id == stage_id)
                    .filter(SceneModel.active == True)
                    .filter(SceneModel.name == name)
                    .first()
                )
                if existedScene:
                    raise Exception(
                        'Scene "{}" already existed. Please choose another name!'.format(
                            name
                        )
                    )
                scene.name = name
            else:
                scene.name = f"Scene {scene_order}"

            local_db_session.add(scene)
            local_db_session.flush()
            local_db_session.commit()

            scene_id = scene.id
            return SaveScene(id=scene_id)


class DeleteScene(graphene.Mutation):
    """Mutation to sweep a stage."""

    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True, description="ID of the scene to be deleted.")

    @jwt_required()
    def mutate(self, info, id):
        with ScopedSession() as local_db_session:
            scene = (
                local_db_session.query(SceneModel).filter(SceneModel.id == id).first()
            )
            if scene:
                code, error, user, timezone = current_user()
                if not user.role in (ADMIN, SUPER_ADMIN):
                    if not user.id == scene.owner_id:
                        return DeleteScene(
                            success=False,
                            message="Only scene owner or admin can delete this scene!",
                        )

                scene.active = False
                local_db_session.flush()
                local_db_session.commit()
            else:
                return DeleteScene(success=False, message="Scene not found!")

        return DeleteScene(success=True, message="Scene deleted successfully!")

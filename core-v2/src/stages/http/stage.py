from ariadne import MutationType, QueryType, make_executable_schema
from core.decorators.authenticated import authenticated
from performance_config.services.performance import PerformanceService
from performance_config.services.scene import SceneService
from stages.graphql.stage import type_defs
from ariadne.asgi import GraphQL

from stages.http.validation import (
    AssignMediaInput,
    AssignStagesInput,
    DuplicateStageInput,
    PerformanceInput,
    RecordInput,
    SceneInput,
    StageInput,
    UpdateMediaInput,
    UploadMediaInput,
)
from stages.services.media import MediaService
from stages.services.stage import StageService
from users.entities.user import ADMIN, PLAYER, SUPER_ADMIN, UserEntity

query = QueryType()
mutation = MutationType()


@mutation.field("createStage")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def create_stage(_, info, input):
    return StageService().create_stage(
        UserEntity(**info.context["request"].state.current_user), StageInput(**input)
    )


@mutation.field("updateStage")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def update_stage(_, info, input):
    return StageService().update_stage(
        UserEntity(**info.context["request"].state.current_user), StageInput(**input)
    )


@mutation.field("deleteStage")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def delete_stage(_, info, id):
    return StageService().delete_stage(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("duplicateStage")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def duplicate_stage(_, info, id: int, name: str):
    return StageService().duplicate_stage(
        UserEntity(**info.context["request"].state.current_user),
        DuplicateStageInput(id=id, name=name),
    )


@mutation.field("assignMedia")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def assign_media(_, info, input: AssignMediaInput):
    return MediaService().assign_media(AssignMediaInput(**input))


@mutation.field("uploadMedia")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def assign_media(_, info, input: UploadMediaInput):
    return MediaService().upload_media(
        UserEntity(**info.context["request"].state.current_user),
        UploadMediaInput(**input),
    )


@mutation.field("updateMedia")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def update_media(_, info, input: UpdateMediaInput):
    return MediaService().update_media(
        UpdateMediaInput(**input),
    )


@mutation.field("deleteMedia")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def delete_media(_, info, id: int):
    return MediaService().delete_media(id)


@mutation.field("assignStages")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def assign_stages(_, info, input: AssignStagesInput):
    return MediaService().assign_stages(AssignStagesInput(**input))


@mutation.field("sweepStage")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def sweep_stage(_, info, id: int):
    return StageService().sweep_stage(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("saveScene")
@authenticated()
def save_scene(_, info, input: SceneInput):
    return SceneService().create_scene(
        UserEntity(**info.context["request"].state.current_user), SceneInput(**input)
    )


@mutation.field("deleteScene")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def delete_scene(_, info, id: int):
    return SceneService().delete_scene(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("updatePerformance")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def update_performance(_, info, input):
    return PerformanceService().update_performance(
        UserEntity(**info.context["request"].state.current_user),
        PerformanceInput(**input),
    )


@mutation.field("deletePerformance")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def delete_performance(_, info, id: int):
    return PerformanceService().delete_performance(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("startRecording")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def start_recording(_, info, input):
    return PerformanceService().create_performance(
        UserEntity(**info.context["request"].state.current_user),
        RecordInput(**input),
    )


@mutation.field("saveRecording")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def save_recording(_, info, id: int):
    return PerformanceService().save_recording(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("updateStatus")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def update_status(_, info, id: int):
    return StageService().update_status(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("updateVisibility")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def update_visibility(_, info, id: int):
    return StageService().update_visibility(
        UserEntity(**info.context["request"].state.current_user), id
    )


@mutation.field("updateLastAccess")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def update_last_access(_, info, id: int):
    return StageService().update_last_access(
        UserEntity(**info.context["request"].state.current_user), id
    )


schema = make_executable_schema(type_defs, query, mutation)
stage_graphql_app = GraphQL(schema, debug=True)

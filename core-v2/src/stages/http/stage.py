from ariadne import MutationType, QueryType, make_executable_schema
from core.decorators.authenticated import authenticated
from stages.graphql.stage import type_defs
from ariadne.asgi import GraphQL

from stages.http.validation import (
    AssignMediaInput,
    AssignStagesInput,
    DuplicateStageInput,
    StageInput,
    UpdateMediaInput,
    UploadMediaInput,
)
from stages.services.media import MediaService
from stages.services.stage import StageService
from users.entities.user import ADMIN, PLAYER, SUPER_ADMIN, UserEntity

query = QueryType()
mutation = MutationType()


@query.field("hello")
def hello(*_):
    return "Hello, world!"


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


schema = make_executable_schema(type_defs, query, mutation)
stage_graphql_app = GraphQL(schema, debug=True)

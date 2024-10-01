from ariadne import MutationType, QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from assets.http.validation import MediaTableInput, SaveMediaInput
from global_config import authenticated
from studios.http.graphql import type_defs
from assets.services.asset import AssetService
from users.db_models.user import ADMIN, PLAYER, SUPER_ADMIN, UserModel

query = QueryType()
mutation = MutationType()


@query.field("mediaList")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def search_assets(_, info, **kwargs):
    return AssetService().get_all_medias(
        UserModel(**info.context["request"].state.current_user), kwargs
    )


@query.field("media")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def search_assets(_, __, **kwargs):
    return AssetService().search_assets(MediaTableInput(**kwargs["input"]))


@mutation.field("uploadFile")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def upload_file(_, __, base64: str, filename: str):
    return AssetService().upload_file(base64, filename)


@mutation.field("saveMedia")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def save_media(_, info, input: SaveMediaInput):
    return AssetService().save_media(
        UserModel(**info.context["request"].state.current_user),
        SaveMediaInput(**input),
    )


@mutation.field("deleteMedia")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def delete_media(_, info, id: int):
    return AssetService().delete_media(
        UserModel(**info.context["request"].state.current_user), id
    )


schema = make_executable_schema(type_defs, query, mutation)
asset_graphql_app = GraphQL(schema, debug=True)

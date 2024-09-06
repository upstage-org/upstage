from ariadne import MutationType, QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from core.decorators.authenticated import authenticated
from studio.graphql.studio import type_defs
from assets.services.asset import AssetService
from users.entities.user import ADMIN, PLAYER, SUPER_ADMIN

query = QueryType()
mutation = MutationType()


@query.field("hello")
def hello(_, info):
    print("aaaa")
    return "Hello World"


@mutation.field("uploadFile")
@authenticated(allowed_roles=[SUPER_ADMIN, ADMIN, PLAYER])
def upload_file(_, __, base64: str, filename: str):
    return AssetService().upload_file(base64, filename)


schema = make_executable_schema(type_defs, query, mutation)
asset_graphql_app = GraphQL(schema, debug=True)
